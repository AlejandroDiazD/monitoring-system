import time
import logging

from src.sensors.sensor_simulator import SensorSimulator

logging.basicConfig(level=logging.INFO)

# Temporal solution for running code from cli: 
# export PYTHONPATH=$(pwd):$PYTHONPATH

def main():

    sensors = [('humidity', 3), ('temperature', 1)]
    sensor_simulator = SensorSimulator(sensors, 'mqtt', 'simulator_client')

    try:
        sensor_simulator.run_threads()
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Simulation stopped.")
        logging.info("Stopping all threads...")
        sensor_simulator.stop_threads()

if __name__ == "__main__":
    main()