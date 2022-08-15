#!/bin/bash

# Install dependencies
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev libcurl4-openssl-dev libjansson-dev libgmp-dev automake git gcc g++ make
# install python3 and python-pip
sudo apt-get install -y python3 python3-pip
# install python3 dependencies from requirements.txt
pip3 install -r requirements.txt
# install by run the install setup.py script
python3 setup.py install
