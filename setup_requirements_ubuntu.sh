#!/usr/bin/env bash

# Sets up requirements FOR UBUNTU

# Python 
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9 python3.9-dev python3.9-venv

sudo apt-get install vagrant virtualbox
sudo apt-get install avahi-daemon libnss-mdns # mDNS name resolution in private network

python3.9 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
