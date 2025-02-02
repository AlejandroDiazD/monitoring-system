import random
import time
import threading
import logging
import json

from src.rabbitmq.mqtt_client_base import MQTTClientBase

class SensorSimulator(MQTTClientBase):

    sensor_types = ('humidity', 'temperature')
    sensors_threads = []
    stop_event = threading.Event()

    def __init__(self, 
                 sensors: list[tuple[str, int]],
                 mode: str = "log",
                 client_id: str = None,
                 broker: str = "localhost",
                 port: int = 1883,
                 keepalive: int = 60):
        super().__init__(broker, port, client_id, keepalive)
        """
        Args:
            sensors: List of sensors to simulate, in which each sensor
                is represented by a tuple with the sensor type and the 
                sensor period: [(sensor_type (str), sensor_period (int))]
            mode: Mode to publish simulated sensors. Modes are ['log', 'mqtt']
            broker: Broker IP in case of using mqtt
            client_id: String with the client_id in case of using mqtt

        An example input to init the class is:
        sensors = [('humidity', 5), ('temperature', 1), ('temperature', 3)]
        """
        self.sensors = self._init_sensors(sensors)
        self.mode = mode
        if mode == "mqtt":
            self._init_mqtt_client(broker, port, client_id, keepalive)
        logging.info(f"Sensor simulator running in '{mode}' mode")
            

    def _validate_sensors(self, sensors: list[tuple[str, int]]
            ) -> list[tuple[str, int]]:
        """
        Validates that sensors input data is correct for sensors 
        definition.

        Args:
            sensors: List of sensors to validate
        
        Returns:
            sensors: List of sensors validated
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
            input_sensors: List of sensors as tuples
                Example: [sensor1, sensor2, ...]
                sensor (tuple): (sensor_type, sensor_period)
        
        Returns:
            output_sensors: List of sensors as dictionaries
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

    def _init_mqtt_client(self, broker: str, port: int, client_id: str, 
                          keepalive: int):
        """
        Validates input parameters and connects to the mqtt broker.
        """
        if broker == None:
            raise ValueError(
                "Broker ip is None, it must be a valid value."
            )
        if not isinstance(broker, str):
            raise TypeError(
                "Broker ip must be a valid value in string format."
            )
        if client_id == None:
            raise ValueError(
                "Client id is None, it must be a valid value."
            )
        if not isinstance(client_id, str):
            raise TypeError(
                "Client id must be a valid value in string format."
            )
        if not isinstance(port, int):
            raise TypeError(
                "Port must be a valid value in int format."
            )
        if not isinstance(keepalive, int):
            raise TypeError(
                "Keepalive must be a valid value in int format."
            )
        self.connect()
        # self.loop_start()

    def generate_sensor_data(self, sensor_type: str, period: int, id: int
                             ) -> dict:
        """
        Generates simulated sensor data.

        Args:
            sensor_type: Type of sensor: temperature or humididy
            id: Sensor id

        Returns:
            Simulated sensor in dictionary format
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
        Gets and publishes sensor data using logs.

        Args:
            sensor_type: Type of sensor ['temperature', 'humididy']
            period: Period in seconds to get and publish the data
            id: Sensor id
            stop_event: Event to signal thread termination

        Returns:
            Publishes sensor data at a given period (freq = 1/period)
        """
        try:
            while not stop_event.is_set():
                data = self.generate_sensor_data(sensor_type, period, id)
                logging.info(f'data received: {json.dumps(data)}')
                time.sleep(period)
            logging.info(f"Thread for sensor {id} stopped.")
        except Exception as e:
            logging.error(f"Error in thread for sensor {id}: {e}")

    def publish_mqtt_sensor(self, sensor_type: str, period: int, id: int,
                            stop_event: threading.Event,
                            topic: str = "test", qos: int = 1, 
                            retain: bool = False):
        """
        Gets and publishes sensor data in a given mqtt topic.

        Args:
            sensor_type: Type of sensor ['temperature', 'humididy']
            period: Period in seconds to get and publish the data
            id: Sensor id
            stop_event: Event to signal thread termination
            topic: MQTT topic to publish data
            qos (optional): Quality of Service level. Defaults to 1
            retain (optional): Whether to retain the message. Defaults to False
        """
        # topic += str(id)
        try:
            while not stop_event.is_set():
                data = self.generate_sensor_data(sensor_type, period, id)
                time.sleep(period)
                self.publish(topic, json.dumps(data), qos, retain)
                logging.info(f'data published: {json.dumps(data)}')
        except Exception as e:
            logging.error(f"Error in thread for sensor {id}: {e}")


    def run_threads(self):
        """
        Creates and starts a different thread for each simulated sensor 
        to publish simulated data. The data can be published using logs
        or using mqtt.
        """
        if   self.mode == 'log' : target=self.print_log_sensor
        elif self.mode == 'mqtt': target=self.publish_mqtt_sensor

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
        Stops and deletes the running threads of simulated sensors. 
        """
        self.stop_event.set()
        for thread in self.sensors_threads:
            thread.join()
        self.sensors_threads.clear()
        logging.info("All threads stopped.")
