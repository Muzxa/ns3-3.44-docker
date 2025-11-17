FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    build-essential
    
RUN add-apt-repository ppa:deadsnakes/ppa -y

RUN apt-get update && apt-get install -y \ 
    python3 \
    python3-venv \
    python3-distutils \
    python3-dev

RUN python3 -m venv .venv
RUN .venv/bin/pip install ns3

RUN apt-get update && apt-get install -y \
    vim \
    wget \
    tar \
    cmake

## YOU CAN COMMENT OUT THIS CODE IF YOU DO NOT WANT TO RUN NS-3 C++ FILES
COPY ./ns-allinone-3.44.tar.bz2 /ns-allinone-3.44.tar.bz2
RUN tar -xjf ns-allinone-3.44.tar.bz2
WORKDIR /ns-allinone-3.44/ns-3.44
RUN ./ns3 configure --enable-examples --enable-tests
RUN ./ns3 build

CMD ["bash"]