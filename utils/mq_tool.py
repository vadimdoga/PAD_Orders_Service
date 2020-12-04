import logging
import json
import pika
import time
from os import environ

from utils.orders.post import update_final_order

logging.getLogger("pika").propagate = False

class MQTool:
    def __init__(self, queue_name):
        for i in range(1, 4):
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=environ["MQ_HOST"]))
                logging.info("Connected to RMQ")
                break
            except pika.exceptions.AMQPConnectionError as err:
                logging.info("Failed to connect to RMQ")
                time.sleep(pow(2, i))
                if i == 3:
                    raise pika.exceptions.AMQPConnectionError(err)
                continue

        self.queue_name = queue_name
        self.connection = connection

    def mq_publish(self, dict_body):
        channel = self.connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_publish(
            exchange='', routing_key=self.queue_name, body=json.dumps(dict_body))
        logging.info(f"Message sent to queue: {self.queue_name}")
        self.connection.close()

    def mq_receive(self):
        def callback(ch, method, properties, body):
            logging.info(f"Message received on {self.queue_name}")
            update_final_order(data_body=body)

        channel = self.connection.channel()
        channel.queue_declare(queue=self.queue_name)

        channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True)

        logging.info(f"{self.queue_name} waiting for message!")
        channel.start_consuming()
