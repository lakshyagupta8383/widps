#pragma once // makes sure that thi header file is only imported once even if we import it multiple time indirectly
#include <string>
#include <vector>
#include <unordered_map>
#include "common.hpp"
using namespace std;

class CsvParser {
public:
    CsvParser();
    bool parseLine(const string &line, ProbeEntry &out); // used by main.cpp to create a parser object and use this method to parse the csv files

private:
    enum Section { NONE, AP_SECTION, STATION_SECTION } currentSection; //0-> NONE, 1->AP_SECTION, 2->STATION_SECTION
    vector<string> headerCols; // all the header extracted from the csv files 
    unordered_map<string,int> colIndex; //a hashmap to map headers to their respective numbers just in case if airodump chnange the order

    // set of functions used by csv_parser.cpp
    void setHeader(const string &line); //converts header line into headerCols and colIndex map(lowercased names->index)
    static string trim(const string &s);
    static vector<string> splitExactlyN(const string &s, size_t n); //splits a line into n coloumns using n-1 comma seperated values
    static bool parseTimestamp(const string &s, long &ts);
    static bool macValid(const string &m);// validats the mac address

    //AP-> access point is wifi router which converts the wireless connection to wired connection to form a wlan
    //Station-> phones,laptop etc with a network interface (to check the network interface run the cmd iw dev in the terminal)
    //below are seperate functions to parse ap and station data seperately

    bool parseAp(const vector<string> &parts, ProbeEntry &out);
    bool parseStation(const vector<string> &parts, ProbeEntry &out);
};
