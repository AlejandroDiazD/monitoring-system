import json
import random
import time
import logging
import threading

# Configurar el logger
logging.basicConfig(level=logging.INFO)

def generate_sensor_data(sensor_type: str, id: int) -> dict:
    """
    Generates simulated sensor data.

    Args:
        sensor_type (str): Type of sensor: temperature or humididy.
        id (int): Sensor id.

    Returns:
        (dict): Simulated sensor in dictionary format
    """
    if sensor_type not in ["temperature", "humidity"]:
        raise ValueError(
            "Sensor type must be one of these: ['temperature', 'humidity'].")
    

    return {
        "sensor_id": f"sensor_{sensor_type}_{id}",
        "type": random.choice(["temperature", "humidity"]),
        "value": round(random.uniform(20.0, 100.0), 2),
        "timestamp": time.time()}
    

def publish_sensor_data(sensor_type: str, id: int, period: int, 
                        stop_event: threading.Event):
    """
    Gets and publishes sensor data.

    Args:
        sensor_type (str): Type of sensor: temperature or humididy.
        id (int): Sensor id.
        period (int): Period to get and publish the data.
        stop_event (Event): Event to signal thread termination.

    Returns:
        Publishes sensor data at a given frequency.
    """
    while not stop_event.is_set():
        data = generate_sensor_data(sensor_type, id)
        logging.info(f'data received: {json.dumps(data)}')
        time.sleep(period)
    logging.info(f"Thread for {sensor_type} sensor {id} stopped.")

def main():
    t_sensors = 1   # Number of temperature sensors to simulate
    h_sensors = 1   # Number of humidity sensors to simulate

    t_period = 1
    h_period = 5

    sensors_threads = []
    stop_event = threading.Event()

    for i in range(t_sensors):
        thread = threading.Thread(
            target = publish_sensor_data,
            args = ('humidity', i, t_period, stop_event)
        )
        sensors_threads.append(thread)

    for j in range(h_sensors):
        thread = threading.Thread(
            target = publish_sensor_data,
            args = ('temperature', i+j, h_period, stop_event)
        )
        sensors_threads.append(thread)

    for thread in sensors_threads:
        thread.start()

    return sensors_threads, stop_event

if __name__ == "__main__":
    try:
        sensors_threads, stop_event = main()
        while True:
                time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Simulation stopped.")
        logging.info("Stopping all threads...")
        stop_event.set()
        for thread in sensors_threads:
            thread.join()
        logging.info("All threads stopped. Simulation exited successfully.")