import pika


class Producer:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def establish_connection(self):
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters('cow.rmq2.cloudamqp.com', credentials=credentials, virtual_host=self.username)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()

    def queue_publish(self, message):
        self.channel.basic_publish(exchange='', routing_key='Output', body=message, properties=pika.BasicProperties(delivery_mode=1))