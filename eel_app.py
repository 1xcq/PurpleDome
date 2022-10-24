import subprocess
import os
import sys
import json
import yaml
import gevent.monkey

gevent.monkey.patch_all()
import eel
from typing import Optional

from app.machinecontrol import Machine
from app.config import CTFEnvironmentConfig
from app.machinequeue import MachineQueue
from app.exceptions import MachineError
from app.attack_log import AttackLog
from plugins.base.machinery import MachineStates


class Challenge:
    def __init__(self, _path):
        self.path = _path
        self.config: Optional[CTFEnvironmentConfig] = None
        self.name: Optional[str] = None
        self.description: Optional[str] = None
        self.targets: list[Machine] = []
        # (steps), hints, quiz

    def setup_machines(self):
        self.targets.clear()
        for target_config in self.config.targets():
            if not target_config.is_active():
                continue
            machine = Machine(target_config, attack_logger=attack_logger)
            if machine is None:
                raise MachineError("Creating target machine failed")
            self.targets.append(machine)

    def list_machines(self) -> list[dict]:
        return [{"name": target.get_name(), "state": target.get_state().name} for target in self.targets]

    def dump_data(self):
        data = {}
        for x in ["path", "name", "description"]:
            data[x] = getattr(self, x)
        print(data)
        return data

    def start(self):
        def start_machine(machine):
            try:
                if not machine.config.use_existing_machine():
                    machine.destroy()  # this can fail if machine does not exist but tried anyway
            except subprocess.CalledProcessError:
                # Maybe the machine just does not exist yet
                pass
            print(f"{machine.get_name()}: Up")
            machine.up()
            machine.reboot()
            needs_reboot = machine.prime_vulnerabilities()
            needs_reboot |= machine.prime_sensors()
            if needs_reboot:
                machine.reboot()
            print(f"{machine.get_name()}: Vulns")
            machine.install_vulnerabilities()
            machine.start_vulnerabilities()
            print(f"{machine.get_name()}: Done")

        mq = MachineQueue(thread_num=4, callback_func=start_machine)
        for target in self.targets:
            mq.put(target)
        mq.join()

    def stop(self):
        def stop_machine(machine):
            machine.stop_sensors()
            machine.stop_vulnerabilities()
            machine.halt()

        mq = MachineQueue(thread_num=4, callback_func=stop_machine)
        for target in self.targets:
            mq.put(target)
        mq.join()


""" 
GLOBAL VARIABLES
"""
running_challenge: Optional[int] = None
attack_logger = AttackLog(1)

file_path = os.path.dirname(__file__)
challenge_dir = os.path.join(file_path, "challenges")
challenges: list[Challenge] = []


def load_challenges():
    global challenges
    challenges = [Challenge(_path=challenge) for challenge in sorted(os.listdir(challenge_dir))]

    for c in challenges:
        config_path = os.path.join(challenge_dir, c.path, "config.yaml")
        c.config = CTFEnvironmentConfig(config_path)
        description_path = os.path.join(challenge_dir, c.path, "description.yaml")
        with open(description_path, encoding="utf8") as fh:
            data = yaml.safe_load(fh)
            if data is None:
                continue
            c.name = data.get("name", "")
            c.description = data.get("description", "")
        c.setup_machines()


@eel.expose
def start_challenge(index):
    global running_challenge
    challenge = challenges[index]
    challenge.start()
    running_challenge = index
    return running_challenge


@eel.expose
def stop_running_challenge():
    global running_challenge
    if running_challenge is None:
        return
    challenge = challenges[running_challenge]
    challenge.stop()
    running_challenge = None


@eel.expose
def list_challenges():
    return [c.dump_data() for c in challenges]


@eel.expose
def list_challenge_machines(index):
    challenge = challenges[index]
    return challenge.list_machines()


@eel.expose
def get_running_challenge():
    global running_challenge
    return running_challenge


def start_eel_server(development: bool):
    """Start Eel in either production or development environment."""

    if development:
        directory = "web-app/src"
        app = None
        page = {'port': 3000}  # point to dev server from svelte app
    else:
        directory = "web-app/public"
        app = 'default'
        page = 'index.html'
    eel.init(directory, allowed_extensions=['.tsx', '.ts', '.jsx', '.js', '.html'])
    eel_kwargs = dict(
        host='localhost',
        port=8080,
    )
    eel.start(page, mode=app, **eel_kwargs)


if __name__ == '__main__':
    environment = os.environ.get('ENV', '')
    load_challenges()
    start_eel_server(development=(environment == 'dev'))
