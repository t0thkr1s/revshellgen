#!/bin/bash

# detect if the OS is linux debian or ubuntu or kali linux, and use the appropriate package manager
if [ -f /etc/debian_version ]; then
    # Debian or Ubuntu or Kali Linux
    sudo apt-get update
    sudo apt-get install -y build-essential libssl-dev libcurl4-openssl-dev libjansson-dev libgmp-dev automake git gcc g++ make
    # install python3 and python-pip
    sudo apt-get install -y python3 python3-pip
else
    # OS not supported
    echo "OS not supported"
    exit 1
fi

# install python3 dependencies from requirements.txt
pip3 install -r requirements.txt
# install by run the install setup.py script
python3 setup.py install
