#include "http_client.hpp"
#include <curl/curl.h>
#include <iostream>
using namespace std;

HttpClient::HttpClient(const string &url) : endpoint(url) {} //saves the backend API endpoint

bool HttpClient::postJson(const string &json)
{
    cout<<json<<endl;
    CURL *c = curl_easy_init(); //initialize the curl object
    if (!c) return false;
    struct curl_slist *h = nullptr;
    h = curl_slist_append(h, "Content-Type: application/json"); //tells curl that a message is to be sent 
    curl_easy_setopt(c, CURLOPT_URL, endpoint.c_str()); //set url to send post request
    curl_easy_setopt(c, CURLOPT_POST, 1L); // mentioning the type of request ->post  (1L=true here as cur expects long int)
    curl_easy_setopt(c, CURLOPT_HTTPHEADER, h); //header is set as ontent-Type: application/json
    curl_easy_setopt(c, CURLOPT_POSTFIELDS, json.c_str()); //sets the body for the post req, c_str() converts it to a C-style string (char*) because cURL is a C library
    curl_easy_setopt(c, CURLOPT_TIMEOUT_MS, 3000L); //req is aborted if the server doesnt responds in 3 sec
    CURLcode r = curl_easy_perform(c); // the req is sent 
    curl_slist_free_all(h); //memory cleanup for headers
    curl_easy_cleanup(c); //destroy the cURL handle
    return r == CURLE_OK; //returns true if the post req is successful
}
