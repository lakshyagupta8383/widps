cmake_minimum_required(VERSION 3.10)
project(sniffer-cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${CMAKE_SOURCE_DIR}/include)

add_executable(sniffer
    src/main.cpp
    src/csv_parser.cpp
    src/event_builder.cpp
    src/http_client.cpp
)

find_package(CURL REQUIRED)
if(CURL_FOUND)
    include_directories(${CURL_INCLUDE_DIRS})
    target_link_libraries(sniffer ${CURL_LIBRARIES})
endif()
