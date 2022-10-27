import pika


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

    def callback(self, ch, method, properties, body):
        """body += deepstack preds"""
        print('Received %r' % body)

    def consume(self):
        self.channel.basic_consume(queue='Input', on_message_callback=self.callback, auto_ack=True)

    def get_message(self):
        return self.message

    def start_consume(self):
        self.channel.start_consuming()



# X = Consumer('vdfnfbub', 'lg96txyrDMmv3Sp0FR5f86GXye9vpCZP')
# X.establish_connection()
# X.consume()
# X.start_consume()
# print(X.get_message())