import os
import subprocess
from typing import Deque
import psutil
import numpy as np
from collections import deque

ID=0
if "ID" in os.environ:
    ID = int(os.environ["ID"])
    
LOOP_TIME = 10
if "LOOP_TIME" in os.environ:
    LOOP_TIME = int(os.environ["LOOP_TIME"])
    
class LogMetrics:
    def __init__(self):
        self.output = ""
        self.endl = " \n"
        
        self.q_len = 10
        self.txs =  Deque(maxlen=self.q_len)
        self.txs_diff = Deque(maxlen=self.q_len)
        self.rxs =  Deque(maxlen=self.q_len)
        self.rxs_diff = Deque(maxlen=self.q_len)
        self.td = LOOP_TIME

    def add_docker_partitition_usage(self, id=ID):
        cmd_output = subprocess.check_output(["df", "-h", "/var/lib/docker"]).decode(
            "utf-8"
        )
        self.output += (
            f"docker_partition_usage_percent{{id=\"{id}\"}} "
            + cmd_output.split("\n")[1].split()[4][:-1]
            + self.endl
        )
        self.output += (
            f"docker_partition_available_gb{{id=\"{id}\"}} "
            + cmd_output.split("\n")[1].split()[3][:-1]
            + self.endl
        )
    def add_system_usage(self, id=ID):
        
        self.output += (
            f"system_memory_usage_percent{{id=\"{id}\"}} "
            + str(psutil.virtual_memory().percent)
            + self.endl
        )
        self.output += (
            f"system_cpu_usage_percent{{id=\"{id}\"}} "
            + str(psutil.cpu_percent())
            + self.endl
        )
        self.output += (
            f"system_cpu_frequency{{id=\"{id}\"}} "
            + str(psutil.cpu_freq().current)
            + self.endl
        )
        
        bytes_sent = psutil.net_io_counters().bytes_sent
        bytes_recv = psutil.net_io_counters().bytes_recv
        self.txs.append(bytes_sent)
        self.rxs.append(bytes_recv)
        
        if len(self.txs) > 2:
            self.txs_diff.append(self.txs[1] - self.txs[0])
            self.rxs_diff.append(self.rxs[1] - self.rxs[0])
            
        if len(self.txs) == self.q_len:
            self.output += (
                f"system_net_bytes_tx_per_sec{{id=\"{id}\"}} "
                + str(np.mean(self.txs_diff)/self.td)
                + self.endl
            )
            self.output += (
                f"system_net_bytes_rx_per_sec{{id=\"{id}\"}} "
                + str(np.mean(self.rxs_diff)/self.td)
                + self.endl
            )
        
        self.output += (
            f"system_net_bytes_tx{{id=\"{id}\"}} "
            + str(bytes_sent)
            + self.endl
        )
        
        self.output += (
            f"system_net_bytes_rx{{id=\"{id}\"}} "
            + str(bytes_recv)
            + self.endl
        )
        
        self.output += (
            f"system_disk_bytes_read{{id=\"{id}\", label=\"ssd\"}} "
            + str(psutil.disk_io_counters(perdisk=True)["sdb"].read_bytes)
            + self.endl
        )
        
        self.output += (
            f"system_disk_bytes_write{{id=\"{id}\", label=\"ssd\"}} "
            + str(psutil.disk_io_counters(perdisk=True)["sdb"].write_bytes)
            + self.endl
        )
        self.output += (
            f"system_disk_bytes_read{{id=\"{id}\", label=\"hdd\"}} "
            + str(psutil.disk_io_counters(perdisk=True)["sda2"].read_bytes)
            + self.endl
        )
        
        self.output += (
            f"system_disk_bytes_write{{id=\"{id}\", label=\"hdd\"}} "
            + str(psutil.disk_io_counters(perdisk=True)["sda2"].write_bytes)
            + self.endl
        )
        
        self.output += (
            f"system_disk_bytes_free{{id=\"{id}\", label=\"hdd\"}} "
            + str(psutil.disk_usage("/mnt/g").free)
            + self.endl
        )
    def __str__(self):
        output = self.output
        self.output = ""
        return output
