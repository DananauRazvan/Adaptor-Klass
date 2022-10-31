import pika
import json
from send_json_rabbit import Producer
from deepstack import DeepStackPrediction
from get_image_redis import ImageRedis
import os
import random
import glob
from logs import logs


"""
Get data from RabbitMQ, a JSON file
"""
class Consumer:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logs = logs('get_data_rabbit.py', 'logs/get_data_rabbit_logs.log')

    def establish_connection(self):
        try:
            self.logs.info('Establish connection with Rabbit Mq, Input queue')

            credentials = pika.PlainCredentials(username=self.username, password=self.password)
            parameters = pika.ConnectionParameters('cow.rmq2.cloudamqp.com', credentials=credentials, virtual_host=self.username)
            connection = pika.BlockingConnection(parameters)
            self.channel = connection.channel()

        except Exception as e:
            self.logs.error('Error occurred in Consumer, establish connection ' + str(e))

    def call_api_deepstack(self):
        try:
            self.logs.info('Call API Deepstack')

            image = random.choice(glob.glob('test_images/*.jpg'))
            print('Image name:', image)

            X = ImageRedis('localhost', '6379', image)
            X.establish_connection()
            X.read_image()
            X.encode_image()
            X.write_redis()
            X.read_from_redis()
            encoded_message = X.get_encoded_image()  #Encoded message read from Redis

            X = DeepStackPrediction(encoded_message)
            X.deepstack_response()

            if X.get_no_objects_detected() > 0:
                self.deepstack_json_message = X.get_object_det_json_response()
                self.has_detected = True
            else:
                self.has_detected = False

        except Exception as e:
            self.logs.error('Error occured when calling API Deepstack ' + str(e))

    def callback(self, ch, method, properties, body):
        try:
            self.logs.info('Callback')

            body = json.loads(body)

            if self.has_detected:
                body.update(self.deepstack_json_message)

            P = Producer('vdfnfbub', 'lg96txyrDMmv3Sp0FR5f86GXye9vpCZP')
            P.establish_connection()
            P.queue_publish(json.dumps(body))

            print('Received: %r' % body)

        except Exception as e:
            self.logs.error('Error occurred in callback ' + str(e))

    def consume(self):
        try:
            self.logs.info('Rabbit consume')

            self.channel.basic_consume(queue='Input', on_message_callback=self.callback, auto_ack=True)

        except Exception as e:
            self.logs.error('Error occurred at consume ' + str(e))

    def start_consume(self):
        try:
            self.logs.info('Start consuming')

            self.channel.start_consuming()

        except Exception as e:
            self.logs.error('Error occurred at start consuming')