import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "test/topic"

client = mqtt.Client()
client.connect(broker, port, 60)

for i in range(10):
    message = f"Mensaje {i}"
    client.publish(topic, message)
    print(f"Publicado: {message}")

client.disconnect()
