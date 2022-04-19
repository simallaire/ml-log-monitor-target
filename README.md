# Introduction 
This project is meant to be used as a target endpoint for prometheus to monitor.
It is meant to be added as a submodule to a container you want to monitor or to run by itself.

# Getting Started
main.py is an incomplete example implementation, here's the necessary steps to have a functionning log monitor target
You may want to check other branches for complete implementations.
1.	Create and start the threaded http server
2.	Create the logmetrics string builder
3.	Call the logmetrics function you added
4.	Write the logmetrics on the server using `server.write(logmetrics)`
5.  Loop

# Build and Test
``` 
python main.py 
```

See `logserver` branch for dockerize implementation

``` 
docker-compose up 
```

# Contribute

Add your new target to `ml-log-monitor/prometheus/prometheus.yml`

(Optional) Add a new rule for your target's metrics in `ml-log-monitor/prometheus/rules.yml`