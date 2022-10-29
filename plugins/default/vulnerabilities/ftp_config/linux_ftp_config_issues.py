#!/usr/bin/env python3

# Allow anonymous access to ftp folder

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class FtpVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "ftp_config_vul"
    description = "Allowing anonymous user access to ftp"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = ["it-security-exam.pdf"]    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def start(self):

        # install ftp server
        install = "sudo apt-get -y install vsftpd"
        self.run_cmd(install)

        # backup conf
        backup = "sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.orig"
        self.run_cmd(backup)

        # allow anonymous access to /var/ftp without password
        config = r"sudo sed -i 's/anonymous_enable=NO/anonymous_enable=YES\nanon_root=\/var\/ftp\nno_anon_password=YES/g' /etc/vsftpd.conf"
        self.run_cmd(config)

        # make ftp folder
        folder = "sudo mkdir /var/ftp && sudo mv /home/vagrant/it-security-exam.pdf /var/ftp/it-security-exam.pdf && sudo chown -R nobody:nogroup /var/ftp"
        self.run_cmd(folder)

        # Restart vsftpd
        restart = "sudo systemctl restart vsftpd"
        self.run_cmd(restart)

    def stop(self):

        # Restore backup config with initial state
        restore = "sudo mv /etc/vsftpd.conf.orig /etc/vsftpd.conf"
        self.run_cmd(restore)

        # Remove ftp folder
        remove = "sudo rm -rf /var/ftp"
        self.run_cmd(remove)

        # Stop vsftpd
        stop = "sudo systemctl stop vsftpd"
        self.run_cmd(stop)
