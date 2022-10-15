import subprocess
import os
import sys
import yaml
import gevent.monkey
gevent.monkey.patch_all()
import eel

from app.machinecontrol import Machine
from app.config import CTFEnvironmentConfig
from app.machinequeue import MachineQueue
from app.exceptions import MachineError
from app.attack_log import AttackLog
from plugins.base.machinery import MachineStates

targets: list[Machine] = []
attack_logger = AttackLog(1)

# exe_path = os.path.abspath(os.path.join(sys.executable, os.pardir))
exe_path = os.path.dirname(__file__)
challenge_path = os.path.join(exe_path, "challenges")
challenges: list[str] = sorted(os.listdir(challenge_path))


def load_config(index):
    config_path = os.path.join(challenge_path, index, "config.py")
    return CTFEnvironmentConfig(config_path)


@eel.expose
def start_environment():
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

    # put all machines into queue and run start_machine in parallel
    mq = MachineQueue(thread_num=4, callback_func=start_machine)
    for target in targets:
        mq.put(target)
    mq.join()


@eel.expose
def stop_environment():
    def stop_machine(machine):
        machine.halt()

    mq = MachineQueue(thread_num=4, callback_func=stop_machine)
    for target in targets:
        mq.put(target)
    mq.join()


@eel.expose
def list_challenges():
    return challenges


@eel.expose
def list_state():
    a = [{"name": target.get_name(), "state": target.get_state().name} for target in targets]
    print(a)
    return a


@eel.expose
def list_machines(index: str):
    if index not in challenges:
        return []
    config = load_config(index)
    targets.clear()
    for target_config in config.targets():
        if not target_config.is_active():
            continue
        machine = Machine(target_config, attack_logger=attack_logger)
        if machine is None:
            raise MachineError("Creating target machine failed")
        targets.append(machine)

    a = [{"name": target.get_name(), "state": target.get_state().name} for target in targets]
    print(a)
    return a


def start_eel_server(development: bool):
    """Start Eel in either production or development environment."""

    if development:
        directory = "static_web_folder/src"
        app = None
        page = {'port': 3000}  # point to dev server from svelte app
    else:
        directory = "static_web_folder/public"
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
    start_eel_server(environment == 'dev')
