#!/usr/bin/env python3

# Some users are created (with weak passwords) and sshd is set to allow password-based access

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class SshdVersionVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "sshd_version_addendum"
    description = "Setting a random sshd version string"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def start(self):
        # set version string
        if self.conf.get('flag'):
            cmd = f"sudo sed -i 's/#VersionAddendum none/VersionAddendum {self.conf.get('flag')}/g' /etc/ssh/sshd_config"
            self.run_cmd(cmd)

        # Restart ssh
        cmd = "sudo service ssh restart"
        self.run_cmd(cmd)

    def stop(self):
        # Re-configure sshd to inital state
        if self.conf.get('flag'):
            cmd = f"sudo sed -i 's/VersionAddendum {self.conf.get('flag')}/#VersionAddendum none/g' /etc/ssh/sshd_config"
            self.run_cmd(cmd)

        # Restart ssh
        cmd = "sudo service ssh restart"
        self.run_cmd(cmd)
