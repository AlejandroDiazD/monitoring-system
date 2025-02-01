import time
import logging

from sensors.sensor_simulator import SensorSimulator

logging.basicConfig(level=logging.INFO)

def main():

    sensors = [('humidity', 3), ('temperature', 1)]
    sensor_simulator = SensorSimulator(sensors)

    try:
        sensor_simulator.run_threads('log')
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Simulation stopped.")
        logging.info("Stopping all threads...")
        sensor_simulator.stop_threads()

if __name__ == "__main__":
    main()