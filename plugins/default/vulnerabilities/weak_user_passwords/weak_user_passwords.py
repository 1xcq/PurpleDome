#!/usr/bin/env python3

# Some users are created (with weak passwords) and sshd is set to allow password-based access

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class WeakPasswordVulnerabilityVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "weak_user_passwords"
    description = "Adding users with weak passwords"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def start(self):
        if self.machine_plugin.config.os() == "linux":
            # Add vulnerable user
            # mkpasswd -m sha-512    # To calc the passwd
            # This is in the debian package "whois"

            for user in self.conf["linux"]:
                add = f"sudo useradd {user['name']} -s /bin/bash -m"
                self.run_cmd(add)
                # useradd needs hashed password, go around that by changing afterwards
                pw = f"echo {user['name']}:{user['password']} | sudo chpasswd"
                self.run_cmd(pw)
                if user.get('flag') is not None:
                    flag_cmd = f"sudo su - {user['name']} -c \"echo {user['flag']} >> /home/{user['name']}/presentation-notes.txt\""
                    self.run_cmd(flag_cmd)

        elif self.machine_plugin.config.os() == "windows":

            for user in self.conf["windows"]:
                # net user username password /add
                cmd = f"net user {user['name']} {user['password']} /add"
                self.run_cmd(cmd)

            for user in self.conf["windows"]:
                # Adding the new users to RDP (just in case we want to test RDP)
                cmd = f"""NET LOCALGROUP "Remote Desktop Users" {user['name']} /ADD"""
                self.run_cmd(cmd)

        else:
            raise NotImplementedError

    def stop(self):
        if self.machine_plugin.config.os() == "linux":
            for user in self.conf["linux"]:
                # flag_cmd = f"sudo rm -rf /home/{user['name']}"
                # self.run_cmd(flag_cmd)
                # Remove user
                cmd = f"sudo userdel -rf {user['name']}"
                self.run_cmd(cmd)

        elif self.machine_plugin.config.os() == "windows":
            for user in self.conf["windows"]:
                # net user username /delete
                cmd = f"net user {user['name']} /delete"
                self.run_cmd(cmd)

            # Remove the new users to RDP (just in case we want to test RDP)
            for user in self.conf["windows"]:
                # net user username /delete
                cmd = f""""NET LOCALGROUP "Remote Desktop Users" {user['name']} /DELETE"""
                self.run_cmd(cmd)

        else:
            raise NotImplementedError
