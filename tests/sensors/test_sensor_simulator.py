import pytest
import threading
import time
import re
import logging

# Import the class to be tested
from src.sensors.sensor_simulator import SensorSimulator

# Fixture to initialize the SensorSimulator with sample sensors
@pytest.fixture
def sensor_simulator():
    sensors = [('humidity', 5), ('temperature', 1)]
    return SensorSimulator(sensors)

# Test _validate_sensors with valid input
def test_validate_sensors_valid_input(sensor_simulator):
    """
    Test _validate_sensors with valid input.
    """
    sensors = [('humidity', 5), ('temperature', 1)]
    validated_sensors = sensor_simulator._validate_sensors(sensors)
    assert validated_sensors == sensors

# Test _validate_sensors with invalid input (not a list)
def test_validate_sensors_invalid_input_not_list(sensor_simulator):
    """
    Test _validate_sensors with invalid input (not a list).
    """
    output = "Sensors values must be a list"
    with pytest.raises(ValueError, match=output):
        sensor_simulator._validate_sensors("not_a_list")

# Test _validate_sensors with invalid input (not a tuple)
def test_validate_sensors_invalid_input_not_tuple(sensor_simulator):
    """
    Test _validate_sensors with invalid input (not a tuple).
    """
    output = "Each sensor must be a tuple of 2 values."
    with pytest.raises(ValueError, match=output):
        sensor_simulator._validate_sensors([['humidity', 5]])

# Test _validate_sensors with invalid input (wrong types)
def test_validate_sensors_invalid_input_wrong_types(sensor_simulator):
    """
    Test _validate_sensors with invalid input (wrong types).
    """
    output = "Each tuple must contain a sensor type (string) and sensor period (int)."
    with pytest.raises(ValueError, match=re.escape(output)):
        sensor_simulator._validate_sensors([(5, 'humidity')])

# Test _validate_sensors with invalid sensor type
def test_validate_sensors_invalid_sensor_type(sensor_simulator):
    """
    Test _validate_sensors with invalid sensor type.
    """
    output = f"Sensor type must be one of: {sensor_simulator.sensor_types}"
    with pytest.raises(ValueError, match=re.escape(output)):
        sensor_simulator._validate_sensors([('invalid_type', 5)])

# Test _init_sensors with valid input
def test_init_sensors(sensor_simulator):
    """
    Test _init_sensors with valid input.
    """
    sensors = [('humidity', 5), ('temperature', 1)]
    initialized_sensors = sensor_simulator._init_sensors(sensors)
    expected_sensors = [
        {'id': 0, 'type': 'humidity', 'period': 5},
        {'id': 1, 'type': 'temperature', 'period': 1}
    ]
    assert initialized_sensors == expected_sensors

# Test generate_sensor_data
def test_generate_sensor_data(sensor_simulator):
    """
    Test generate_sensor_data.
    """
    data = sensor_simulator.generate_sensor_data('humidity', 5, 0)
    assert 'id' in data
    assert 'type' in data
    assert 'period' in data
    assert 'value' in data
    assert 'timestamp' in data
    assert data['type'] == 'humidity'
    assert data['period'] == 5
    assert data['id'] == 0

# Test print_log_sensor
def test_print_log_sensor(sensor_simulator, caplog):
    """
    Test print_log_sensor.
    """
    caplog.set_level(logging.INFO)
    stop_event = threading.Event()
    thread = threading.Thread(
        target=sensor_simulator.print_log_sensor,
        args=('humidity', 1, 0, stop_event)
    )
    thread.start()
    time.sleep(2)  # Allow time for the thread to log data
    stop_event.set()
    thread.join()
    assert 'data received' in caplog.text

# Test run_threads
def test_run_threads(sensor_simulator):
    """
    Test run_threads.
    """
    sensor_simulator.run_threads(mode='log')
    assert len(sensor_simulator.sensors_threads) == 2
    sensor_simulator.stop_threads()

# Test stop_threads
def test_stop_threads(sensor_simulator):
    """
    Test stop_threads.
    """
    sensor_simulator.run_threads(mode='log')
    sensor_simulator.stop_threads()
    for thread in sensor_simulator.sensors_threads:
        assert not thread.is_alive()