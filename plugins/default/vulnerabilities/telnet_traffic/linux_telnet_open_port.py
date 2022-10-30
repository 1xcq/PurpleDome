#!/usr/bin/env python3

# Allow anonymous access to ftp folder

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class TelnetVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "telnet_open_port"
    description = "Allow access to telnet port"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def start(self):

        # install telnet server
        install = "sudo apt-get -y install telnetd"
        self.run_cmd(install)

        # Banner
        banner = 'echo "I am a coffee machine!" | sudo tee /etc/issue.net'
        self.run_cmd(banner)

        # Restart telnetd
        restart = "sudo systemctl start inetd"
        self.run_cmd(restart)

    def stop(self):

        # Stop telnetd
        stop = "sudo systemctl stop inetd"
        self.run_cmd(stop)
