import json
import logging
from os import environ

import pika

from utils.orders.post import update_final_order

logging.getLogger("pika").propagate = False
logger = logging.getLogger(__name__)


class MQTool:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.channel = self.init_channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        logger.info("Connected to RMQ")

    def init_channel(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=environ["MQ_HOST"],
                                      connection_attempts=3,
                                      retry_delay=2))
        return connection.channel()

    def close_connection(self):
        self.connection.close()

    def mq_publish(self, dict_body):

        def send():
            self.channel.basic_publish(exchange='',
                                       routing_key=self.queue_name,
                                       body=json.dumps(dict_body))
            logger.info(f"Message sent to queue: {self.queue_name}",
                        extra={"transaction_id": dict_body["transaction_id"]})

        try:
            send()
        except pika.exceptions.StreamLostError:
            logger.info(f"Restart connection for queue: {self.queue_name}")
            self.channel = self.init_channel()
            send()

    def mq_receive(self):
        def callback(ch, method, properties, body):
            logger.info(f"Message received on {self.queue_name}")
            update_final_order(data_body=body, q_name=method.routing_key)

        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True)

        logger.info(f"{self.queue_name} waiting for message!")
        self.channel.start_consuming()
