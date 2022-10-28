import pika
import json
from send_json_rabbit import Producer

"""
Get data from RabbitMQ, a JSON file
"""
class Consumer:
    def __init__(self, username, password, json_predictions):
        self.username = username
        self.password = password
        self.json_predictions = json_predictions

    def establish_connection(self):
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters('cow.rmq2.cloudamqp.com', credentials=credentials, virtual_host=self.username)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()

    def callback(self, ch, method, properties, body):
        body = json.loads(body)
        body.update(self.json_predictions)

        P = Producer('vdfnfbub', 'lg96txyrDMmv3Sp0FR5f86GXye9vpCZP')
        P.establish_connection()
        # P.queue_out()
        P.queue_publish(json.dumps(body))

        print('Received: %r' % body)

    def consume(self):
        self.channel.basic_consume(queue='Input', on_message_callback=self.callback, auto_ack=True)

    def start_consume(self):
        self.channel.start_consuming()