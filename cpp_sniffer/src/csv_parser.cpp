#include "csv_parser.hpp"
#include <sstream>
#include <iomanip>
#include <ctime>
#include <cctype>

using namespace std;

CsvParser::CsvParser() : currentSection(NONE) {} // constructor defined with default value as none(0)

string CsvParser::trim(const string &s) { 
    size_t a = 0; //size_t-> non negative values
    while (a < s.size() && isspace((unsigned char)s[a])) ++a; // increments the value of if s[a] is empty space to eliminate spaces before the line starts
    size_t b = s.size();
    while (b > a && isspace((unsigned char)s[b-1])) --b; // decrements the value of if s[b] is empty space to eliminate spaces after the line ends
    return s.substr(a, b - a); // finally return the string after eliminating spaces in the start and the end 
}

vector<string> CsvParser::splitExactlyN(const string &s, size_t n) {
    vector<string> out;
    out.reserve(n); // capcity of the vector out is n
    if (n == 0) return out; // returning empty vector if n is 0
    string field; //to store each comma seperated value
    stringstream ss(s); // stream initialized to extract cols in upcoming snippet
    for (size_t i = 0; i < n - 1; ++i) {
        if (!getline(ss, field, ',')) field.clear(); //uses getline to read characters from the stringstream ss into the field string until a comma delimiter is found
        out.push_back(trim(field)); // the value is pushed to out vector after trimming to maintain consistency
    }
    //the parser interprets n parameters to be parsed but just in case if airodump changes anything anf number of parameters are increased or decreased,that is handled below
    //in case the parameters are inccreased then we combine all paramenters and add them as one
    //else if they are decreased we add empty strings
    string last;
    if (getline(ss, last)) out.push_back(trim(last));
    else out.push_back(string());
    while (out.size() < n) out.push_back(string());
    return out;
}
// check the validity of a mac addr  i.e. 6 pairs of colon seperated hexa values
bool CsvParser::macValid(const string &m) {
    if (m.size() != 17) return false; //6*2=12 + 5 colons=12
    for (size_t i = 0; i < m.size(); ++i) { 
        if ((i % 3) == 2) { //every third element is a colon
            if (m[i] != ':') return false;
        } else {
            if (!isxdigit((unsigned char)m[i])) return false; // check for hexadecimal value 
        }
    }
    return true;
}
// function to parse timestamp(ts) from a string 
bool CsvParser::parseTimestamp(const string &s, long &ts) {
    if (s.empty()) { ts = time(nullptr); return false; } // if stirng is empty then ts is null and func returns 0
    tm t{}; // an in-built class in cpp for time 
    istringstream iss(s);// so parse ts from the given string 
    iss >> get_time(&t, "%Y-%m-%d %H:%M:%S");
    if (iss.fail()) { ts = time(nullptr); return false; } // again if ts the ts is not successfully parsed then ts is null and func returns 0
    ts = mktime(&t); //converts tm ds to long ds
    return true;
}

void CsvParser::setHeader(const string &line) {
    //clears the prev records
    headerCols.clear(); 
    colIndex.clear();
    size_t commas = 0;
    // count the number of commas to the calculate the value of number of columns
    for (char c : line) if (c == ',') ++commas;
    size_t cols = commas + 1;
    headerCols = splitExactlyN(line, cols); //uses splitExactlyN method to put all the headers in an array
    for (size_t i = 0; i < headerCols.size(); ++i) {
        
        string k = headerCols[i];
        for (auto &ch : k) ch = (char)tolower((unsigned char)ch);
        k = trim(k);
        colIndex[k] = (int)i;
    }
    string first = headerCols.empty() ? string() : headerCols[0]; //if the headerCol vector is empty then an empty string is assigned to first, else the first element is assigned to first
    string firstLower = first;
    for (auto &ch : firstLower) ch = (char)tolower((unsigned char)ch);
    //acc to the first element the type of section is decided
    if (firstLower.find("bssid") != string::npos) currentSection = AP_SECTION; //if first element is bssid-> the section is an AP
    else if (firstLower.find("station mac") != string::npos) currentSection = STATION_SECTION;// if first element is station mac> the section is an STATION
    else currentSection = NONE;
}

bool CsvParser::parseAp(const vector<string> &p, ProbeEntry &out) {
    // lambda used to find the index of the col name from colIndex
    auto idx = [&](const string &name)->int {
        string n = name;
        for (auto &c : n) c = (char)tolower((unsigned char)c);
        if (!colIndex.count(n)) return -1; //if n is not found in the map then the lambda returns -1
        return colIndex.at(n); //if found in the map the lambda returns the index val
    };
    //obtaining the index val of all the cols
    int iBssid = idx("bssid");
    int iPower = idx("power");
    int iEssid = idx("essid");
    int iLast = idx("last time seen");
    int iChannel = idx("channel");
    if (iBssid < 0 || iBssid >= (int)p.size()) return false; //checking wheather the idx of bssid is >=0 and < the length of the p/parts array
    string mac = p[iBssid]; //obtianing mac via ibssid idx
    if (!macValid(mac)) return false; //validating the mac address
    //setting the values inside the probeEntry
    out.type = "ap";
    out.mac = mac;
    out.ssid = (iEssid >= 0 && iEssid < (int)p.size()) ? p[iEssid] : string(); //if idx of iEssid is within bounds of the p array then the value is set inside the probeEntry, else an empty stirng is used
    if (iPower >= 0 && iPower < (int)p.size()) { // checks that iPower is within bounds 
        try { out.signal = stoi(p[iPower]); } catch(...) { out.signal = 0; } //if the stoi() method fails for some reason then the val 0 is set in the probeEntry
    } else out.signal = 0; // if the idx is out of bounds
    long ts = time(nullptr); //initializing the ts with the current time val
    if (iLast >= 0 && iLast < (int)p.size()) parseTimestamp(p[iLast], ts); //if ts idx is within bounds then the it is parsed otherwise the current time val will be used
    out.timestamp = ts; //setting probe val
    // just like power checks are made for channel as well (within bounds check and string to int conversion)
    if (iChannel >= 0 && iChannel < (int)p.size()) { 
        try { out.channel = stoi(p[iChannel]); out.has_channel = true; } catch(...) { out.channel = 0; out.has_channel = false; }
    } else { out.channel = 0; out.has_channel = false; }
    out.assoc_bssid.clear(); //no assoc_bssid for ap
    return true;
}



bool CsvParser::parseStation(const vector<string> &p, ProbeEntry &out) {
// same lambda for getting col idx
auto idx = [&](const string &name)->int {
string n = name;
for (auto &c : n) c = (char)tolower((unsigned char)c);
if (!colIndex.count(n)) return -1;
return colIndex.at(n);
};


// getting all needed idx vals
int iStation = idx("station mac");
int iPower = idx("power");
int iProbed = idx("probed essids");
int iLast = idx("last time seen");
int iBssid = idx("bssid");


// station mac is mandatory
if (iStation < 0 || iStation >= (int)p.size()) return false;


string mac = p[iStation]; // getting mac val
if (!macValid(mac)) return false; // validating


out.type = "station";
out.mac = mac;
out.ssid = (iProbed >= 0 && iProbed < (int)p.size()) ? p[iProbed] : string(); // inserting probed essids if valid


// parsing power same as ap
if (iPower >= 0 && iPower < (int)p.size()) {
try { out.signal = stoi(p[iPower]); } catch(...) { out.signal = 0; }
} else out.signal = 0;


long ts = time(nullptr); // default ts
if (iLast >= 0 && iLast < (int)p.size()) parseTimestamp(p[iLast], ts); // parsing timestamp if valid
out.timestamp = ts;


out.assoc_bssid = (iBssid >= 0 && iBssid < (int)p.size()) ? p[iBssid] : string(); // station may have assoc bssid


out.channel = 0; // station does not use channel
out.has_channel = false;
return true;
}




bool CsvParser::parseLine(const string &line, ProbeEntry &out) {
string s = trim(line); // removing extra spaces
if (s.empty()) return false; // ignore blank lines


string low = s;
for (auto &c : low) c = (char)tolower((unsigned char)c); // creating lowercase copy for checking header


// checking if the line is a header (bssid or station mac)
if (low.rfind("bssid,", 0) == 0 || low.rfind("station mac,", 0) == 0) {
setHeader(s); // setting header cols and colIndex
return false; // header is not data
}


// no section selected yet or header missing
if (currentSection == NONE || headerCols.empty()) return false;


// splitting line into parts based on header count
auto parts = splitExactlyN(s, headerCols.size());


// based on the current section we parse ap or station
if (currentSection == AP_SECTION) return parseAp(parts, out);
if (currentSection == STATION_SECTION) return parseStation(parts, out);


return false; // nothing else to parse
}
