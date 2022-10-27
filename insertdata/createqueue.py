import pika

credentials = pika.PlainCredentials('vdfnfbub', 'lg96txyrDMmv3Sp0FR5f86GXye9vpCZP')
parameters = pika.ConnectionParameters('cow.rmq2.cloudamqp.com', credentials=credentials, virtual_host='vdfnfbub')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare("Input", passive=False, durable=True, exclusive=False, auto_delete=False,  arguments={'x-max-length': 5000,"x-queue-mode":"default"})
channel.queue_declare("Output", passive=False, durable=True, exclusive=False, auto_delete=False,  arguments={'x-max-length': 5000,"x-queue-mode":"default"})