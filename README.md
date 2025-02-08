# Deployment Guide

## How to publish simulated sensor data in the RabbitMQ broker using MQTT?
### 1. Run a RabbitMQ docker container

### 2. Run sensor simulator script
1. Add the root path of the repository to the python path if necessary:
> export PYTHONPATH="$(pwd):$PYTHONPATH"
2. Run the sensor simulator script:
> python3 src/main.py