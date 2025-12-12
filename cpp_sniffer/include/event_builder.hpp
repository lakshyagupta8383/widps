#pragma once
#include <string>
#include "common.hpp"
using namespace std;

class EventBuilder {
public:
    string buildJson(const ProbeEntry &e); //takes probeEntry as an argument and returns a json object for the sames
};
