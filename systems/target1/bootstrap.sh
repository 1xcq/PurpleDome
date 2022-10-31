#!/usr/bin/env bash

# Bootstrap the new VM
#
#

# Update system
apt update
apt -y upgrade

apt -y install apt-transport-https
apt -y install net-tools
apt -y install openssh-server
apt -y install avahi-daemon # local hostname resolution between the hosts
apt -y install libnss-mdns # ^^^
apt -y install whois # for mkpasswd
apt -y install libprotobuf-dev
apt -y install libbpf-dev
apt -y install gdb
apt -y install openbsd-inetd tcpd

apt -y update
apt -y upgrade


# ip addr show enp0s8 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1 > /vagrant/target3/ip4.txt
hostname -I | cut -d " " -f2 > /vagrant/target1/ip4.txt
# reboot
