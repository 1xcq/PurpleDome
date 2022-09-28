# PurpleDome Capture-the-Flag

This fork of PurpleDome contains a lot of changes that make the project more suitable for CTF use.

I do **not** recommend using it in Online-Events as the virtual machines PurpleDome sets up with Vagrant are insecure by design. (Standard Credentials)

The changes so far mainly serve the purpose as a Network-Lab to learn and try out new concepts.

## Installation

On a current Ubuntu 21.10 system, just execute the *init.sh* to install the required packages and set up the virtual env.

You need python 3.9

**If you do not have python 3.9, have a look at pyenv**

Another option on Ubuntu is to install the python3.9 package with apt-get via the deadsnakes/ppa source. 

It will not run properly in a VM unless VT-x is available, as it spawns own VMs. We confirmed it is working in VirtualBox. Please reserve enough disk space. The simple ctf_world configfile will already download an ubuntu image an create 2 VMs. They must be stored on your VM.

```bash
./init.sh
```

Default vms will be vagrant and virtualbox.

*Make sure the virtual environment has been created with the correct python version (have a look into `venv/bin/`)*

**Before using any PurpleDome commands switch into the python environment:**

```bash
source venv/bin/activate
```

## Setting up the CTF environment

**Make sure you are in the python3.9 virtual environment**
   - (check if all requirements are installed) 

```bash
python3 ./ctf_control.py -vv  run --configfile ctf_world
```

**This will:**

- Use vagrant to setup targets
- Run the targets
- Install all the challenges on the targets
- Keep the targets up to solve the challenges until the script is stopped (CTRL-C)

**Building the machines from vagrant will take some time. Please be patient.**

### Potential issues

#### Vagrantfile Network Bridge

The vagrant configuration uses a bridged public_network shared between the VirtualBox VMs. 

If you do not have one or yours has a different name, please create one and change the config. 

Currently every machine tries to use the default gateway for your local network.

To set a specific interface adapter, uncomment the entry in `/systems/network.settings.yaml` and put in your interface name. (Example: enp3s0, eth0, wl1, ...)
Useful: `ip addr sh`

#### Static ip-addresses

As a default dhcp is used to configure the vagrant machines inside the network.

If dhcp fails and `/systems/target/ip4.txt` does not exist, is empty or has an ipv6 address -> Uncomment the static ips in `/systems/network.settings.yaml` or set your own.

#### Use private network

If you do not want your vulnerable VMs to be accessible from other machines inside your local network you can use a host-only network to access them. 

**This will some break challenges.**

To activate private_network set "use_private" in `/systems/network.settings.yaml` to true.

#### Vagrant machine creation

If creating the target machines fails, you can manually do the step to check why it fails.

```
cd systems
vagrant up target3
vagrant ssh target3
# do something on the VM via ssh
exit
vagrant destroy target3
```

#### Connection issues because of ip-address
When vagrant provisions the boxes (on the first run), it saves the ip-address of the machine.
This step can fail if the network configuration varies a lot.

For CTF-purposes first try to scan your network if the machines exist.

If this does not help look into `systems/target/ip4.txt` for the saved address. If the file is empty / not there see if the hostname -I command in `bootstrap.sh` works when you manually up a machine.

# Upstream PurpleDome related

## PurpleDome creates simulated systems which hack each other

It creates several virtual machines to simulate a target network. A Kali attacker will be spawned and use configured attacks to blast at the targets. Those attacks can be Kali command line tools, Caldera abilities or Metasploit tools.

The goal is to test sensors and detection logic on the targets and in the network and improve them.

The system is at the same time reproducible and quite flexible (target system wise, vulnerabilities on the targets, attacks).

## Running the basic commands

All command line tools have a help included. You can access it by the "--help" parameter

```
python3 ./experiment_control.py -v  run
```

* -v is verbosity. To spam stdout use -vvv
* run is the default command
* --configfile <filename> is optional. If not supplied it will take experiment.yaml

Most of the configuration is done in the yaml config file. For more details check out the full documentation

## Testing

Basic code and unit tests can be run by

```
make test
```

That way you can also see if your env is set up properly.

It will also check the plugins you write for compatibility.

the tool

```
./pydantic_test.py
```

is *not* included in the make test. But you can use it manually to verify your yaml config files. As they tend to become quite complex this is a time safer.

## More documentation

This README is just a short overview. In depth documentation can be found in the *doc* folder.

Documentation is using sphinx. To compile it, go into this folder and call

```
make html
```

Use your browser to open build/html/index.html and start reading.

## Development

The code is stored in [https://github.com/avast/PurpleDome](https://github.com/avast/PurpleDome). Feel free to fork it and create a pull request.

Development happens in *feature branches* branched of from *develop* branch. And all PRs go back there.
The branch *release* is a temporary branch from *develop* and will be used for bug fixing before a PR to *main* creates a new release. Commits in main will be marked with tags and the *changelog.txt* file in human readable form describe the new features.

https://nvie.com/posts/a-successful-git-branching-model/

Short:

* As a user, the *main* branch is relevant for you
* Start a feature branch from *develop*
* When doing a hotfix, branch from *main*

### GIT

Branching your own feature branch

```
$ git checkout development
$ git pull --rebase=preserve
$ git checkout -b my_feature
```

Do some coding, commit.

Rebase before pushing

```
$ git checkout development
$ git pull --rebase=preserve
$ git checkout my_feature
$ git rebase development
```

Code review will be happening on github. If everything is nice, you should squash the several commits you made into one (so one commit = one feature). This will make code management and debugging a lot simpler when you commit is added to develop and main branches

```
git rebase --interactive
git push --force
```

### Argcomplete

https://kislyuk.github.io/argcomplete/

Is a argparse extension that registers the command line arguments for bash. It requires a command line command to register it globally. This is added to init.sh

The configuration will be set in /etc/bash_completion.d/ . Keep in mind: It will require a shell restart to be activated

## BibTeX

When doing scientific research using Purple Dome, please use this BibTeX snippet in your paper:

```
@misc{PurpleDome:internet,
author = {Thorsten Sick and Fabrizio Biondi},
title = {GitHub - avast/PurpleDome: Simulation environment for attacks on computer networks},
note = {(visited on 09.02.2022)},
howpublished = "\url{https://github.com/avast/PurpleDome}",
}
```
