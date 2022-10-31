# Scan your targets

## Preparation 

- install nmap



## Getting the flag

Scan the network with "nmap <NETWORK-IP>/24"
Scan the machine with "nmap <MACHINE-IP/HOSTNAME> (-Pn)" -Pn skips host discovery if nmap thinks the system is offline because of a firewall
Experiment a bit with other scans "nmap <MACHINE-IP/HOSTNAME> (-Pn) -O -T5"

Find the flag by using version detection on the ssh port (or all) "nmap <MACHINE-IP/HOSTNAME> (-Pn) -p 22 -sV"  
