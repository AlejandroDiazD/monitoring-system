docker run -d --name rabbitmq-mqtt \
  -p 15672:15672 \  # Management console port
  -p 1883:1883 \    # MQTT port
  -p 5672:5672 \    # AMQP port
  rabbitmq:management

##############################################
# Follow these commands to enable mqtt plugin:
##############################################
# docker exec -it rabbitmq-mqtt bash
# rabbitmq-plugins enable rabbitmq_mqtt
# exit

