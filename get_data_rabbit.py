import pika
import json
from send_json_rabbit import Producer
from deepstack import DeepStackPrediction
from get_image_redis import ImageRedis

"""
Get data from RabbitMQ, a JSON file
"""
class Consumer:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def establish_connection(self):
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters('cow.rmq2.cloudamqp.com', credentials=credentials, virtual_host=self.username)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()

    def call_api_deepstack(self):
        X = ImageRedis('localhost', '6379', 'test_images/test_image.jpg')
        X.establish_connection()
        X.read_image()
        X.encode_image()
        X.write_redis()
        X.read_from_redis()
        encoded_message = X.get_encoded_image()  # Encoded message read from Redis

        X = DeepStackPrediction(encoded_message)
        X.deepstack_response()
        self.deepstack_json_message = X.get_object_det_json_response()

    def callback(self, ch, method, properties, body):
        body = json.loads(body)
        body.update(self.deepstack_json_message)

        P = Producer('vdfnfbub', 'lg96txyrDMmv3Sp0FR5f86GXye9vpCZP')
        P.establish_connection()
        # P.queue_out()
        P.queue_publish(json.dumps(body))

        print('Received: %r' % body)

    def consume(self):
        self.channel.basic_consume(queue='Input', on_message_callback=self.callback, auto_ack=True)

    def start_consume(self):
        self.channel.start_consuming()