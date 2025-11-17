# NS-3 Docker

# Prerequisites
- Docker (https://www.docker.com/get-started)
- Git    (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

# Optional Docker Setup 
If you don't want to use .cc (C++ programs), you can comment out the following lines in the Dockerfile to save some space:

```Dockerfile
COPY ./ns-allinone-3.44.tar.bz2 /ns-allinone-3.44.tar.bz2
RUN tar -xjf ns-allinone-3.44.tar.bz2
WORKDIR /ns-allinone-3.44/ns-3.44
RUN ./ns3 configure --enable-examples --enable-tests
RUN ./ns3 build
```

This will reduce the image size and speed up the build process significantly, but you will only be able to run Python scripts.

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/Muzxa/ns3-3.44-docker.git
cd ns3-3.44-docker
```

## Build The Docker Image

```bash
./build.sh
```

Or manually (If you are on windows, this is necessary):

```bash
docker build --platform linux/amd64 -t ubuntu22.04-amd64 .
```

This will take some time, so please be patient.

## Run

```bash
./start.sh
```

Or manually (If you are on windows, this is necessary):

```bash
docker run --platform linux/amd64 -it -v ./volume:/ns-allinone-3.44/ns-3.44/volume ubuntu22.04-amd64 bash
```

## Usage

### Python Scripts

Inside the container:

```bash
source /.venv/bin/activate
cd /ns-allinone-3.44/ns-3.44/volume
python3 first.py
```

### C++ Programs

Inside the container:

```bash
cd /ns-allinone-3.44/ns-3.44/
cp volume/first.cc scratch/first.cc
./ns3 run scratch/first
```

## Notes

- The `volume/` directory is mounted into the container for easy file access
- Python environment is available at `/.venv/`
- NS-3 C++ installation is at `/ns-allinone-3.44/ns-3.44/`
