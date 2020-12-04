import pika
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='ORDER_DELIVERY', durable=False)

channel.basic_publish(exchange='',
                      routing_key='ORDER_DELIVERY',
                      body=json.dumps({
                          "transaction_id": "1228fe2d-cf2a-4d0c-94c2-f37cfc31181b",
                          "user_id": 3,
                          "total_price": 25.2,
                          "products": [
                              {
                                  "product_id": "a2ed23r",
                                  "product_title": "Harry Potter Wand",
                                  "amount": 2
                              }
                          ]
                      }))
print(" [x] Sent json")

connection.close()
