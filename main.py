from httpserver import MyServer
from logmetrics import LogMetrics
import time
import os

LOOP_TIME = 10
if "LOOP_TIME" in os.environ:
    LOOP_TIME = int(os.environ["LOOP_TIME"])


def main():
    server = MyServer()
    log_metrics = LogMetrics()
    
    while True:
        # Build metrics string
        log_metrics.add_docker_partitition_usage()
        log_metrics.add_system_usage()

        server.write(log_metrics)
        time.sleep(LOOP_TIME)


main()
