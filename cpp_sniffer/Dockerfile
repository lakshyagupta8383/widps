#using ubuntu as it has all the library and the image would be light in weight
FROM ubuntu:22.04 

#install build tools + curl
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libcurl4-openssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

#copy source code
COPY . .

#build the image
RUN cmake -S . -B build && cmake --build build -j

#default command
CMD ["./build/sniffer"]
