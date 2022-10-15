# A basic example config file opening 3 challenges
#

###
# List of targets
targets:
  - name: target2
    vm_controller:
      vm_type: vagrant
      vagrantfilepath: systems

    ###
    # simple switch if targets is used in attack simulation. Default is true. If set to false the machine will not be started
    active: yes

    vm_name: target2

    nicknames:

    os: linux
    ###
    # Targets need a unique PAW name for caldera
    paw: target2
    ###
    # Targets need to be in a group for caldera
    group: red_linux

    machinepath: target2
    # Do not destroy/create the machine: Set this to "yes".
    use_existing_machine: yes

    ###
    # The folder all the implants will be installed into
    playground: /home/vagrant

    # Sensors to run on this machine
    sensors:

    vulnerabilities:
      - sshd_config_vul
      - weak_user_passwords

###
# General sensor config config
sensor_conf:

###
# Settings for the results being harvested
results:
  ###
  # The directory the loot will be in
  loot_dir: loot
