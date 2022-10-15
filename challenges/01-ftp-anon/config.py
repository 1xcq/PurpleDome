# A basic example config file opening 3 challenges
#

###
# List of targets
targets:
  - name: target1
    vm_controller:
      vm_type: vagrant
      vagrantfilepath: systems

    ###
    # simple switch if targets is used in attack simulation. Default is true. If set to false the machine will not be started
    active: yes

    vm_name: target1

    nicknames:

    os: linux
    ###
    # Targets need a unique PAW name for caldera
    paw: target1
    ###
    # Targets need to be in a group for caldera
    group: red_linux

    machinepath: target1
    # Do not destroy/create the machine: Set this to "yes".
    use_existing_machine: yes

    ###
    # The folder all the implants will be installed into
    playground: /home/vagrant

    # Sensors to run on this machine
    sensors:

    vulnerabilities:
      - ftp_config_vul

###
# General sensor config config
sensor_conf:

###
# Settings for the results being harvested
results:
  ###
  # The directory the loot will be in
  loot_dir: loot
