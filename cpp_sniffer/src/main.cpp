#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <chrono>
#include <atomic>
#include <deque>
#include <csignal>
#include <cerrno>
#include <system_error>
#include "common.hpp"
#include "csv_parser.hpp"
#include "event_builder.hpp"
#include "http_client.hpp"

using namespace std;
using namespace std::chrono_literals;

static atomic<bool> g_running(true); // atomic is used to prevent concurrent access to a variable

void signal_handler(int)
{
    g_running.store(false);
} // act as a lock free solution for reader-writer problem for variable g_running

// the OS sends signal like SIGINT and SIGTERM when the user press ctrl+c or the system kills the program, signal_handler makes the sure that the program is not shut down
// immediately and the exit is clean(i.e data is flushed properly)

int main(int argc, char **argv)
{
    if (argc < 3)
    {
        return 1;
    }
    string csvPath = argv[1];
    string endpoint = argv[2];

    CsvParser parser;                // instance for parser
    EventBuilder builder;            // instance for builer(json)
    HttpClient httpClient(endpoint); // instance to send data to api endpoint

    deque<string> retryQueue;
    ifstream file;
    streampos lastPos = 0;

    signal(SIGINT, signal_handler);  // sends signal to signal_handler when the user presses ctrl+c
    signal(SIGTERM, signal_handler); // when the process is is killed by the system

    // openFile() function is used to open up a file which may be required several times
    auto openFile = [&](bool seekEnd) -> bool
    {
        if (file.is_open())
            file.close(); // closes the old file (defind above ifstream file)
        file.open(csvPath, ios::in);
        if (!file.is_open())
            return false;
        if (seekEnd)
        {
            file.seekg(0, ios::end); // if file is already filled with prev content, we are going to ignore that content
            lastPos = file.tellg();
        }
        else
        {
            file.seekg(0, ios::beg);
            lastPos = file.tellg();
        }
        return true;
    };

    if (!openFile(true))
    { // checks if the openFile returns true and the the file is open
        error_code ec(errno, generic_category());
        cerr << "Failed to open CSV file '" << csvPath << "': " << ec.message() << "\n";
        return 2;
    }

    const auto pollInterval = 500ms;
    size_t loopCounter = 0;

    while (g_running.load())
    { // till no signal is sent
        ++loopCounter;

        if (!file.good())
        { // checks if the file is in "good state" i.e there are no errors
            if (!openFile(true))
            {
                cerr << "Reopen failed, will retry in 1s\n";
                this_thread::sleep_for(1s);
                continue;
            }
        }
        file.clear(); // if we re-open a file in case of error, it is neccessary to clear up the prev error flags
        file.seekg(0, ios::end);
        streampos endPos = file.tellg();

        // airodump deletes or truncates the CSV and creates a new one with the same name,called rotation so to make sure
        // that they are no issues we check the endPos and lastPos
        if (endPos < lastPos)
        {
            file.close();
            if (!openFile(false))
            {
                cerr << "File rotated but reopen failed\n";
                this_thread::sleep_for(1s);
                continue;
            }
            lastPos = file.tellg();
            cerr << "Detected file rotation/truncate. Reopened and reset position.\n";
        }

        if (endPos > lastPos)
        { // reading the new lines
            file.clear();
            file.seekg(lastPos);
            string line;
            while (getline(file, line))
            {
                lastPos = file.tellg();
                if (line.empty())
                    continue;
                ProbeEntry entry;
                if (!parser.parseLine(line, entry))
                {                                                     // parse the csv line into a probe struct
                    cerr << "Parser rejected line: " << line << "\n"; // checks for error
                    continue;
                }
                string json = builder.buildJson(entry); // conversion of struct to json
                bool ok = httpClient.postJson(json);    // checks if the conversion was successful or not
                if (!ok)
                { // incase of unsuccessful conversion, the struct is pushed into the retryQueue
                    retryQueue.push_back(json);
                    cerr << "POST failed, queued for retry. Queue size: " << retryQueue.size() << "\n";
                }
            }
        }
        // previous failed conversion are retried after every line is read
        if (!retryQueue.empty())
        {
            for (auto it = retryQueue.begin(); it != retryQueue.end();)
            {
                bool ok = httpClient.postJson(*it); // recheck
                if (ok)
                {
                    it = retryQueue.erase(it); // if the retry wass successful, the struct is removed
                }
                else
                {
                    ++it; // for unsuccessful retries, the struct are held in the queue
                }
                if (!g_running.load())
                    break; // incase of termination
            }
            if (!retryQueue.empty())
            {
                cerr << "Retry queue size after attempt: " << retryQueue.size() << "\n"; // prints the number of remaining structs
            }
        }

        if (loopCounter % 120 == 0)
        {
            cerr << "Heartbeat: running. Retry queue size: " << retryQueue.size() << "\n";
        } // after 120 loops(approx 1 min) a message is printed that the sniffer is still alive and the number of struct left
        this_thread::sleep_for(pollInterval); // after on cycle is ended, the sniffer paused for 500ms to prevent 100% CPU usage
    }
    // exactly the part for which we used the signal_handler so that the unsuccessful conversions get one more chance before the system shuts down
    cerr << "Shutting down, attempting to flush " << retryQueue.size() << " queued events\n";
    for (const auto &j : retryQueue)
    {
        bool ok = httpClient.postJson(j);
        if (!ok)
        {
            cerr << "Final flush failed for an event; it will be lost on shutdown\n";
        }
    }

    cerr << "Exited cleanly\n";
    return 0;
}
