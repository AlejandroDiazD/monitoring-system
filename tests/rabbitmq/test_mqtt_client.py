import pytest
from unittest.mock import MagicMock, patch
from src.rabbitmq.mqtt_client_base import MQTTClientBase

@pytest.fixture
def mqtt_client():
    """
    Fixture to create an instance of MQTTClientBase for testing.
    """
    return MQTTClientBase("test.mosquitto.org")

def test_connect(mqtt_client):
    """
    Test the connect method to ensure it calls the client's connect
    function correctly.
    """
    with patch.object(mqtt_client.client, 'connect', return_value=0) as mock_connect:
        mqtt_client.connect()
        mock_connect.assert_called_once_with("test.mosquitto.org", 1883, 60)

def test_disconnect(mqtt_client):
    """
    Test the disconnect method to ensure it calls the client's disconnect 
    function correctly.
    """
    with patch.object(mqtt_client.client, 'disconnect') as mock_disconnect:
        mqtt_client.disconnect()
        mock_disconnect.assert_called_once()

def test_subscribe(mqtt_client):
    """
    Test the subscribe method to ensure it calls the client's subscribe 
    function correctly.
    """
    with patch.object(mqtt_client.client, 'subscribe') as mock_subscribe:
        mqtt_client.subscribe("test/topic", qos=1)
        mock_subscribe.assert_called_once_with("test/topic", 1)

def test_unsubscribe(mqtt_client):
    """
    Test the unsubscribe method to ensure it calls the client's 
    unsubscribe function correctly.
    """
    with patch.object(mqtt_client.client, 'unsubscribe') as mock_unsubscribe:
        mqtt_client.unsubscribe("test/topic")
        mock_unsubscribe.assert_called_once_with("test/topic")

def test_publish(mqtt_client):
    """
    Test the publish method to ensure it calls the client's publish 
    function correctly.
    """
    with patch.object(mqtt_client.client, 'publish') as mock_publish:
        mqtt_client.publish("test/topic", "test message", qos=1, retain=True)
        mock_publish.assert_called_once_with("test/topic", "test message", 1, True)

def test_loop_start(mqtt_client):
    """
    Test the loop_start method to ensure it calls the client's loop_start 
    function correctly.
    """
    with patch.object(mqtt_client.client, 'loop_start') as mock_loop_start:
        mqtt_client.loop_start()
        mock_loop_start.assert_called_once()

def test_loop_stop(mqtt_client):
    """
    Test the loop_stop method to ensure it calls the client's loop_stop 
    function correctly.
    """
    with patch.object(mqtt_client.client, 'loop_stop') as mock_loop_stop:
        mqtt_client.loop_stop()
        mock_loop_stop.assert_called_once()

def test_on_connect(mqtt_client):
    """
    Test the on_connect callback to ensure it logs a successful connection.
    """
    mock_logger = MagicMock()
    mqtt_client.logger = mock_logger
    mqtt_client.on_connect(None, None, None, 0)
    mock_logger.info.assert_called_with("Connected to MQTT Broker successfully.")

def test_on_message(mqtt_client):
    """
    Test the on_message callback to ensure it logs received messages 
    correctly.
    """
    mock_logger = MagicMock()
    mqtt_client.logger = mock_logger
    mock_message = MagicMock()
    mock_message.topic = "test/topic"
    mock_message.payload.decode.return_value = "test message"
    mqtt_client.on_message(None, None, mock_message)
    mock_logger.info.assert_called_with("Received message on test/topic: test message")