#!/usr/bin/env python3

# Some users are created (with weak passwords) and sshd is set to allow password-based access

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class QuoteVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "quote_of_the_day"
    description = "Opens server that sends back a random Quote"
    ttp = ""
    references = [""]

    required_files = ["qotd", "qotd.service"]    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def start(self):
        # start service
        cmd = "sudo chown root:root qotd && sudo cp qotd.service /etc/systemd/system && sudo systemctl enable qotd.service && sudo systemctl daemon-reload && sudo systemctl start qotd.service"
        self.run_cmd(cmd)

    def stop(self):
        # disable service
        cmd = "sudo systemctl disable qotd.service && sudo systemctl stop qotd.service"
        self.run_cmd(cmd)

        # delete script
        cmd = "sudo rm -rf qotd"
        self.run_cmd(cmd)
