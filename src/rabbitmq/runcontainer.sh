docker run -d --name rabbitmq \
  -p 15672:15672 \
  -p 1883:1883 \
  -p 5672:5672 \
  rabbitmq:3-management

# -p 15672:15672 \  # Management console port
# -p 1883:1883 \    # MQTT port
# -p 5672:5672 \    # AMQP port

##############################################
# Follow these commands to enable mqtt plugin:
##############################################
# docker exec -it rabbitmq-mqtt bash
# rabbitmq-plugins enable rabbitmq_mqtt
# exit

