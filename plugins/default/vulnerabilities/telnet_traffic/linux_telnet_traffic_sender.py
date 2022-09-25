#!/usr/bin/env python3

# Allow anonymous access to ftp folder

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class TelnetSendVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "telnet_traffic_sender"
    description = "Allow access to telnet port"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = ["access_telnet.sh"]    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def start(self):

        # install telnet client
        install = "sudo apt-get -y install telnet"
        self.run_cmd(install)

        # setup cron to run script every minute
        cron = 'echo "*/1 * * * * /home/vagrant/access_telnet.sh | telnet 192.168.2.251" | crontab -'
        self.run_cmd(cron)

    def stop(self):

        # remove script from cron
        remove = 'crontab -r'
        self.run_cmd(remove)
