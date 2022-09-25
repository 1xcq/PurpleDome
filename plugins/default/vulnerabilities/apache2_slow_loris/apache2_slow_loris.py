#!/usr/bin/env python3

# Allow anonymous access to ftp folder

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class ApacheVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "apache2_slow_loris"
    description = "Setup apache server that is vulnerable to slow loris attack"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = ["apache_index.html", "publish-flag.sh", "flag-publish.service"]    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def install(self, machine_plugin: None):
        # install apache2 server
        install = "sudo apt-get -y install apache2"
        self.run_cmd(install)


    def start(self):

        # mv index
        move = "sudo mv /home/vagrant/apache_index.html /var/www/html/index.html"
        self.run_cmd(move)

        # Restart apache2
        restart = "sudo systemctl restart apache2"
        self.run_cmd(restart)

        # flag service
        flag = "sudo chown root:root publish-flag.sh && sudo cp flag-publish.service /etc/systemd/system && sudo systemctl enable flag-publish && sudo systemctl daemon-reload && sudo systemctl start flag-publish"
        self.run_cmd(flag)



    def stop(self):

        stop = "sudo systemctl stop apache2"
        self.run_cmd(stop)
