import random
import time
import threading
import logging
import json

class SensorSimulator():

    sensor_types = ('humidity', 'temperature')
    sensors_threads = []
    stop_event = threading.Event()

    def __init__(self, 
                 sensors: list[tuple[str, int]]):
        """
        Args:
            sensors (list): [(sensor_type (str), sensor_period (int))]

        An example input to init a class object is:
        sensors = [('humidity', 5), ('temperature', 1), ('temperature', 3)]
        """
        self.sensors = self._init_sensors(sensors)

    def _validate_sensors(self, sensors: list[tuple[str, int]]
            ) -> list[tuple[str, int]]:
        """
        Validates that sensors input data is correct for sensors 
        definition.

        Args:
            sensors (list[tuple[str, int]]): List of sensors to validate
        
        Returns:
            sensors (list[tuple[str, int]]): List of sensors validated
        """
        if not isinstance(sensors, list):
            raise ValueError("Sensors values must be a list")
        
        for item in sensors:
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError(
                    "Each sensor must be a tuple of 2 values."
                )
            if not isinstance(item[0], str) or not isinstance(item[1], int):
                raise ValueError(
                    "Each tuple must contain a sensor type (string) and sensor period (int)."
                )
            if item[0] not in self.sensor_types:
                raise ValueError(
                    f"Sensor type must be one of: {self.sensor_types}")

        return sensors

    def _init_sensors(self, input_sensors: list[tuple[str, int]]
            ) -> list[dict[int, str, int]]:
        """
        Validates input sensors and returns them as a list of dictionaries.

        Args:
            input_sensors (list): List of sensors as tuples
                Example: [sensor1, sensor2, ...]
                sensor (tuple): (sensor_type, sensor_period)
        
        Returns:
            output_sensors (list): List of sensors as dictionaries
                Example: [sensor1, sensor2, ...]
                sensor (dict): {id: int, sensor_type: str, sensor_period: int}
        """
        output_sensors = []
        sensors = self._validate_sensors(input_sensors)
        
        for i, sensor in enumerate(sensors):
            output_sensor = {
                'id': i,
                'type': sensor[0],
                'period': sensor[1]
            }
            output_sensors.append(output_sensor)
            logging.info(f"Sensors successfully initialized: {json.dumps(output_sensor)}")

        return output_sensors

    def generate_sensor_data(self, sensor_type: str, period: int, id: int
                             ) -> dict:
        """
        Generates simulated sensor data.

        Args:
            sensor_type (str): Type of sensor: temperature or humididy.
            id (int): Sensor id.

        Returns:
            (dict): Simulated sensor in dictionary format
        """
        return {
            "id": id,
            "type": sensor_type,
            "period": period, 
            "value": round(random.uniform(20.0, 100.0), 2),
            "timestamp": time.time()}

    def print_log_sensor(self, sensor_type: str, period: int, id: int,
                        stop_event: threading.Event):
        """
        Gets and publishes sensor data.

        Args:
            sensor_type (str): Type of sensor: temperature or humididy.
            id (int): Sensor id.
            period (int): Period in seconds to get and publish the data.
            stop_event (Event): Event to signal thread termination.

        Returns:
            Publishes sensor data at a given period (freq = 1/period).
        """
        try:
            while not stop_event.is_set():
                data = self.generate_sensor_data(sensor_type, period, id)
                logging.info(f'data received: {json.dumps(data)}')
                time.sleep(period)
            logging.info(f"Thread for sensor {id} stopped.")
        except Exception as e:
            logging.error(f"Error in thread for sensor {id}: {e}")

    def publish_mqtt_sensor(self, *args, **kwargs):
        """
        TODO
        """
        raise NotImplementedError("MQTT publishing is not implemented yet.")

    def run_threads(self, mode='log'):
        """
        """
        if   mode == 'log' : target=self.print_log_sensor
        elif mode == 'mqtt': target=self.publish_mqtt_sensor

        for sensor in self.sensors:
            thread = threading.Thread(
                target = target,
                args = (sensor['type'], sensor['period'], sensor['id'], 
                        self.stop_event)
            )
            self.sensors_threads.append(thread)

        for thread in self.sensors_threads:
            thread.start()
    
    def stop_threads(self):
        """
        """
        self.stop_event.set()
        for thread in self.sensors_threads:
            thread.join()
        self.sensors_threads.clear()
        logging.info("All threads stopped.")
