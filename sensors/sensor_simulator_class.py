class SensorSimulator():

    sensor_types = ('humidity', 'temperature')

    def __init__(self, sensors: list[tuple[str, int]]):
        self.sensors = self._validate_sensors(sensors)

    def _validate_sensors(self, sensors: list[tuple[str, int]]
            ) -> list[tuple[str, int]]:
        """
        Validates that sensors input data is correct for sensors 
        definition. The correct format is a list of tuples with
        type and frequency of the sensor.
        E.g.: [('humidity', 5), ('temperature', 1), ('temperature', 3)]

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
                    """Each tuple must contain a sensor type (string) and 
                    sensor frequency (int)."""
                )
            if item[0] not in self.sensor_types:
                raise ValueError(
                    f"Sensor type must be one of: {self.sensor_types}")

        return sensors


