import paho.mqtt.client as mqtt
import logging
import time

class MQTTClientBase:
    """
    Base class for an MQTT client with standard functionalities.
    This class can be inherited by other classes to extend its functionality.
    """

    def __init__(self, broker: str, port: int = 1883, client_id: str = None, keepalive: int = 60):
        """
        Initialize the MQTT client.

        Args:
            broker: MQTT broker address
            port: MQTT broker port (default: 1883)
            client_id: Unique client ID (default: None - auto-generated)
            keepalive: Keepalive interval in seconds (default: 60)
        """
        self.broker = broker
        self.port = port
        self.client_id = client_id or f"mqtt_client_{int(time.time())}"
        self.keepalive = keepalive
        
        self.client = mqtt.Client(
            client_id=self.client_id, 
            callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when the client connects to the broker."""
        if rc == 0:
            self.logger.info("Connected to MQTT Broker successfully.")
        else:
            self.logger.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        """Callback when the client disconnects from the broker."""
        self.logger.info("Disconnected from MQTT Broker.")

    def on_message(self, client, userdata, message):
        """Callback when a message is received."""
        self.logger.info(f"Received message on {message.topic}: {message.payload.decode()}")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """Callback when a subscription is successful."""
        self.logger.info(f"Subscribed successfully, MID: {mid}, QoS: {granted_qos}")

    def on_publish(self, client, userdata, mid):
        """Callback when a message is published."""
        self.logger.info(f"Message published successfully, MID: {mid}")
    
    def connect(self):
        """Connect to the MQTT broker."""
        self.client.connect(self.broker, self.port, self.keepalive)
    
    def disconnect(self):
        """Disconnect from the MQTT broker."""
        self.client.disconnect()
    
    def subscribe(self, topic: str, qos: int = 0):
        """Subscribe to a topic."""
        self.client.subscribe(topic, qos)
    
    def unsubscribe(self, topic: str):
        """Unsubscribe from a topic."""
        self.client.unsubscribe(topic)
    
    def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False):
        """Publish a message to a topic."""
        self.client.publish(topic, payload, qos, retain)
    
    def loop_start(self):
        """Start the MQTT network loop in a separate thread."""
        self.client.loop_start()
    
    def loop_stop(self):
        """Stop the MQTT network loop."""
        self.client.loop_stop()
    
    def loop_forever(self):
        """Run the network loop forever (blocking)."""
        self.client.loop_forever()

# Example usage:
# class MyMQTTClient(MQTTClientBase):
#     def on_message(self, client, userdata, message):
#         super().on_message(client, userdata, message)
#         print(f"Custom processing: {message.payload.decode()}")
#
# client = MyMQTTClient("broker.hivemq.com")
# client.connect()
# client.loop_start()
# client.subscribe("test/topic")