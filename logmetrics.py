import os
import subprocess
class LogMetrics:
    def __init__(self):
        self.output = ""
        self.endl = " \n"

    def add_docker_partitition_usage(self):
        cmd_output = subprocess.check_output(["df", "-h", "/var/lib/docker"]).decode("utf-8")
        self.output += "docker_partition_usage_percent{id=0} " + cmd_output.split("\n")[1].split()[4][:-1] + self.endl
        self.output += "docker_partition_available_gb{id=0} " + cmd_output.split("\n")[1].split()[3][:-1] + self.endl


    def __str__(self):
        return self.output