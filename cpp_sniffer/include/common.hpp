#pragma once // makes sure that thi header file is only imported once even if we import it multiple time indirectly
#include <string>
using namespace std;

struct ProbeEntry
{
    string type; // "ap" or "station"
    string mac;  // media access control addr (may be randomized to avoid long term tracking by the device)
    int signal;  // Received Signal Strength Indicator — measured in dBm (negative values). Used to estimate distance and link uality
    string ssid; // Service Set Identifier -> name of the wireless network
    long timestamp;
    string assoc_bssid; // Basic Service Set Identifier — the MAC address of the AP's radio interface that identifies the BSS.
    int channel;        // various channel are used, 1/6/11 fro 2.4GHz and multiple for 5GHz
    bool has_channel;   // some rows have has_channel instead of channel so on of the value is set null
    string sniffer_id;  // laptop_01, laptop_02 ......
};
