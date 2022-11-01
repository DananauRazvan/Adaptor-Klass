import pika
from logs import logs


class Producer:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logs = logs('send_json_rabbit.py', 'logs/send_json_rabbit_logs.log')

    def establish_connection(self):
        try:
            self.logs.info('Establish connection with Rabbit Mq, Output queue')

            credentials = pika.PlainCredentials(username=self.username, password=self.password)
            parameters = pika.ConnectionParameters('cow.rmq2.cloudamqp.com', credentials=credentials, virtual_host=self.username)
            connection = pika.BlockingConnection(parameters)
            self.channel = connection.channel()

        except Exception as e:
            self.logs.error('Error occured in Producer, establish connection ' + str(e))

    def queue_publish(self, message):
        try:
            self.logs.info('Basic publish')

            self.channel.basic_publish(exchange='', routing_key='Output', body=message, properties=pika.BasicProperties(delivery_mode=1))

        except Exception as e:
            self.logs.error('Error occurred in basic publish')