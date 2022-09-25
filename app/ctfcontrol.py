#!/usr/bin/env python3

""" A class to control a whole experiment. From setting up the machines to running the attacks """

import os
import subprocess
import time
import zipfile
import shutil
from datetime import datetime
from typing import Optional

from app.attack_log import AttackLog
from app.config import CTFEnvironmentConfig
from app.interface_sfx import CommandlineColors
from app.exceptions import ServerError, CalderaError, MachineError, PluginError, ConfigurationError
from app.pluginmanager import PluginManager
from app.doc_generator import DocGenerator
from app.calderacontrol import CalderaControl
from app.machinecontrol import Machine
from plugins.base.attack import AttackPlugin
from app.machinequeue import MachineQueue



class ChallengeControl():
    """ Class handling challenges """

    def __init__(self, configfile: str, verbosity: int = 0) -> None:
        """

        :param configfile: Path to the configfile to load
        :param verbosity: verbosity level between 0 and 3
        """
        self.start_time: str = datetime.now().strftime("%Y_%m_%d___%H_%M_%S")  #: time the experiment started
        self.loot_dir: str = "loot"  #: Directory to store the loot into. Will be fetched from config

        self.targets: list[Machine] = []  #: A list of target machines

        self.experiment_config = CTFEnvironmentConfig(configfile)
        self.attack_logger = AttackLog(verbosity)
        self.plugin_manager = PluginManager(self.attack_logger)

    def run(self) -> None:
        """
        Run the challenges

        :return:
        """

        self.start_time = datetime.now().strftime("%Y_%m_%d___%H_%M_%S")
        self.loot_dir = os.path.join(self.experiment_config.loot_dir(), self.start_time)
        os.makedirs(self.loot_dir)

        # start target machines
        self.start_target_machines()

        # Add running machines to log
        self.add_running_machines_to_log()

    def stop(self) -> None:
        # stop sensor plugins
        zip_this = []
        for a_target in self.targets:
            a_target.stop_sensors()
            zip_this += a_target.collect_sensors(self.loot_dir)

        # Uninstall vulnerabilities
        for a_target in self.targets:
            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE} Uninstalling vulnerabilities on {a_target.get_paw()} {CommandlineColors.ENDC}", 1)
            a_target.stop_vulnerabilities()
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN} Done uninstalling vulnerabilities on {a_target.get_paw()} {CommandlineColors.ENDC}", 1)

        # Stop target machines
        for target_1 in self.targets:
            target_1.halt()

        self.attack_logger.post_process()
        attack_log_file_path = os.path.join(self.loot_dir, "attack.json")
        self.attack_logger.write_json(attack_log_file_path)
        #document_generator = DocGenerator()
        #document_generator.generate(attack_log_file_path)
        #document_generator.compile_documentation()
        #zip_this += document_generator.get_outfile_paths()
        self.zip_loot(zip_this)

    def add_running_machines_to_log(self) -> None:
        """ Add machine infos for targets and attacker to the log """
        for target in self.targets:
            if target is None:
                raise MachineError("Target machine configured to None or whatever happened")
            i = target.get_machine_info()
            i["role"] = "target"
            self.attack_logger.add_machine_info(i)


    def start_machine(self, machine_info):
        machine_name = machine_info["name"]
        machine_conf = machine_info["config"]
        machine = Machine(machine_conf, attack_logger=self.attack_logger)
        if machine is None:
            raise MachineError("Creating target machine failed")
        try:
            if not machine_conf.use_existing_machine():
                machine.destroy()  # this can fail if machine does not exist but tried anyway
        except subprocess.CalledProcessError:
            # Maybe the machine just does not exist yet
            pass

        machine.up()
        print("before reboot")
        machine.reboot()  # Kernel changes on system creation require a reboot
        print("after reboot")

        needs_reboot = machine.prime_vulnerabilities()
        print("after prime vulns")
        needs_reboot |= machine.prime_sensors()
        print("after prime sens")

        if needs_reboot:
            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}rebooting target {machine_name} ....{CommandlineColors.ENDC}", 1)
            machine.reboot()

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Target is up: {machine_name}  {CommandlineColors.ENDC}", 1)
        self.targets.append(machine)

        self.attack_logger.vprint(f"Installing vulnerabilities on {machine_name}", 2)
        machine.install_vulnerabilities()
        machine.start_vulnerabilities()

        self.attack_logger.vprint(f"Installing sensors on {machine_name}", 2)
        machine.install_sensors()
        machine.start_sensors()

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Target is ready: {machine_name}  {CommandlineColors.ENDC}",1)

    def start_target_machines(self) -> None:
        """ Start target machines

        """
        mq = MachineQueue(thread_num=4, callback_func=self.start_machine)
        for target_conf in self.experiment_config.targets():
            # skip if marked as inactive in CTF config
            if not target_conf.is_active():
                continue
            target_name = target_conf.vmname()
            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}preparing target {target_name} ....{CommandlineColors.ENDC}", 1)
            machine_info = { "name": target_name, "config": target_conf}
            mq.put(machine_info)

        mq.join()


    def zip_loot(self, zip_this: list[str]) -> None:
        """ Zip the loot together

        :param zip_this: A list of file paths to add to the zip file
        """

        filename = os.path.join(self.loot_dir, self.start_time + ".zip")

        self.attack_logger.vprint(f"Creating zip file {filename}", 1)

        with zipfile.ZipFile(filename, "w") as zfh:
            for a_file in zip_this:
                if a_file != filename:
                    self.attack_logger.vprint(a_file, 2)
                    zfh.write(a_file)

            zfh.write(os.path.join(self.loot_dir, "attack.json"))

        # For automation purpose we copy the file into a standard file name
        default_name = os.path.join(self.loot_dir, "..", "most_recent.zip")
        shutil.copyfile(filename, default_name)