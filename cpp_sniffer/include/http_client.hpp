#pragma once
#include <string>
using namespace std;

class HttpClient {
public:
    HttpClient(const string &url);
    bool postJson(const string &json);

private:
    string endpoint;
};