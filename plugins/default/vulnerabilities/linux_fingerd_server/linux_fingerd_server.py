
#!/usr/bin/env python3

# Some users are created (with weak passwords) and sshd is set to allow password-based access

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class FingerdVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "fingerd_service"
    description = "Setup deprecated server"
    ttp = ""
    references = [""]

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def install(self, machine_plugin: None):
        # install package
        install = "sudo apt-get -y install fingerd"
        self.run_cmd(install)

    def start(self):
        # restart inetd
        cmd = "sudo systemctl restart inetd"
        self.run_cmd(cmd)

    def stop(self):
        # disable inetd
        cmd = "sudo systemctl disable inetd && sudo systemctl stop inetd"
        self.run_cmd(cmd)
