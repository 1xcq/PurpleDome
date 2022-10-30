# Purple Dome CTF

## Requirements

Running on Ubuntu is recommended in order to automate the setup. Other Linux flavours will work with the correct packages.

- virtualbox
- vagrant 
- python 3.9
- (avahi-daemon, libnss-mdns)

## Installation

Run the setup script. It will install the necessary packages and setup the python virtual environment as well as install all python requirements.

```bash 
./setup_requirements_ubuntu.sh
``` 

Make sure it created the virtualenv with the correct python version. (3.9)

```bash 
venv/bin/python --version
``` 

## Start CTF

```bash 
./run_ctf_app.sh
``` 

This will source the virtual environment and run the webapp that provides a frontend and allows you to start/stop challenges and submit flags.
On start the app loads all Purple Dome configurations for the challenges and should open in your default browser. (localhost + port 8080)

**When starting your first challenge be patient!**
Purple Dome has to download the VM, update and install the requirements and setup the vulnerabilities.

## Tips & Tricks

- for the private network make sure that virtualbox has a network interface on your machine with ```ip addr sh``` (for example "vboxnet0")

- if the default network settings do not work for you, you can edit ```systems/network.settings.yaml``` to use a bridged network instead of a private one or set static ips instead 

- if the machines are not accessible over network also check ```systems/target/ip4.txt``` for an address

- if creating a machine fails you can manually go through the steps and see where it fails
```
cd systems
vagrant up target1
vagrant ssh target1
# validate commands work
vagrant destroy target1
```