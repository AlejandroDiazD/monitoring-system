# tests/test_sensor_simulator.py

import pytest
from src.sensors.sensor_simulator import SensorSimulator

class TestSensorSimulator:
    """
    Test cases for the SensorSimulator class.
    """

    def test_valid_sensors(self):
        """
        Test that the class accepts and stores a valid list of sensors.
        """
        sensors = [('humidity', 5), ('temperature', 1)]
        sensor_simulator = SensorSimulator(sensors)
        assert sensor_simulator.sensors == sensors

    def test_invalid_sensors_not_a_list(self):
        """
        Test that a ValueError is raised if the input is not a list.
        """
        with pytest.raises(ValueError) as exc_info:
            SensorSimulator("not_a_list")
        assert str(exc_info.value) == "Sensors values must be a list"

    def test_invalid_sensors_not_a_tuple(self):
        """
        Test that a ValueError is raised if any sensor is not a tuple.
        """
        with pytest.raises(ValueError) as exc_info:
            SensorSimulator([('humidity', 5), 'not_a_tuple'])
        assert str(exc_info.value) == "Each sensor must be a tuple of 2 values."

    def test_invalid_sensors_tuple_length(self):
        """
        Test that a ValueError is raised if any tuple does not have exactly 
        2 values.
        """
        with pytest.raises(ValueError) as exc_info:
            SensorSimulator([('humidity', 5, 'extra_value')])
        assert str(exc_info.value) == "Each sensor must be a tuple of 2 values."

    def test_invalid_sensor_type_not_string(self):
        """
        Test that a ValueError is raised if the sensor type is not a string.
        """
        with pytest.raises(ValueError) as exc_info:
            SensorSimulator([(123, 5)])  # 123 is not a string
        assert "Each tuple must contain a sensor type (string)" in str(exc_info.value)

    def test_invalid_sensor_frequency_not_int(self):
        """
        Test that a ValueError is raised if the sensor frequency is not an 
        integer.
        """
        with pytest.raises(ValueError) as exc_info:
            SensorSimulator([('humidity', 'not_an_int')])  # 'not_an_int' is not an int
        assert "sensor frequency (int)" in str(exc_info.value)

    def test_invalid_sensor_type_not_in_allowed_types(self):
        """
        Test that a ValueError is raised if the sensor type is not in the 
        allowed types.
        """
        with pytest.raises(ValueError) as exc_info:
            SensorSimulator([('invalid_type', 5)])  # 'invalid_type' is not allowed
        expected_msg = f"Sensor type must be one of: {SensorSimulator.sensor_types}"
        assert expected_msg in str(exc_info.value)