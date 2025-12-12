#include "event_builder.hpp"

using namespace std;

static string escape_json(const string &s)
{
    string out;
    out.reserve(s.size());
    // converting all the special char from cpp string to valid json escape seq
    for (char c : s)
    {
        if (c == '\\')
            out += "\\\\";
        else if (c == '"')
            out += "\\\"";
        else if (c == '\b')
            out += "\\b";
        else if (c == '\f')
            out += "\\f";
        else if (c == '\n')
            out += "\\n";
        else if (c == '\r')
            out += "\\r";
        else if (c == '\t')
            out += "\\t";
        else
            out += c;
    }
    return out;
}

string EventBuilder::buildJson(const ProbeEntry &e)
{
    // creating json object by escaping each value from the ProbeEntry
    string j = "{";
    j += "\"type\":\"" + escape_json(e.type) + "\",";
    j += "\"mac\":\"" + escape_json(e.mac) + "\",";
    j += "\"signal\":" + to_string(e.signal) + ",";
    if (e.ssid.empty())
        j += "\"ssid\":null,";
    else
        j += "\"ssid\":\"" + escape_json(e.ssid) + "\",";
    j += "\"timestamp\":" + to_string(e.timestamp) + ",";
    if (e.assoc_bssid.empty())
        j += "\"assoc_bssid\":null,";
    else
        j += "\"assoc_bssid\":\"" + escape_json(e.assoc_bssid) + "\",";
    if (e.has_channel)
        j += "\"channel\":" + to_string(e.channel) + ",";
    else
        j += "\"channel\":null,";
    j += "\"sniffer_id\":\"" + escape_json(e.sniffer_id) + "\"";
    j += "}";
    return j;
}
