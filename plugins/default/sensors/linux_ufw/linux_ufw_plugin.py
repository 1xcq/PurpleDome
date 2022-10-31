#!/usr/bin/env python3

# A plugin to experiment with Linux logstash filebeat sensors
# https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation-configuration.html

from plugins.base.sensor import SensorPlugin


class LinuxUFWPlugin(SensorPlugin):
    # Boilerplate
    name = "ufw"
    description = "Linux ufw plugin"

    required_files = []

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__
        self.debugit = False

    def start(self):
        self.run_cmd("sudo ufw allow 22")
        self.run_cmd("sudo ufw --force enable")
        for rule in self.conf.get('allow', []):
            self.run_cmd(f"sudo ufw allow {rule}")

    def stop(self):
        """ Stop the sensor """
        self.run_cmd("sudo ufw disable")
        return
