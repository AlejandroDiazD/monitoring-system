"""
NOT WORKING!! PENDING TO FIX THI SCRIPT.
"""
import pika
import logging

# Connect to RabbitMQ using AMQP
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

exchange = "amq.topic"
queue = "mqtt_queue"
routing_key = "simulated_sensors/"

# Create the queue
channel.queue_declare(queue=queue, durable=True)

# Bind the queue to the amq.topic exchange
channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

logging.info(f"Mqtt queue created and binded. Exchange = {exchange}, Queue = {queue}, Routing_key = {routing_key}")

# Cerrar conexión
connection.close()
