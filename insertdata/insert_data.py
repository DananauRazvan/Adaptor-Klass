import logging
import pika
import time
from pika.exchange_type import ExchangeType


credentials = pika.PlainCredentials('vdfnfbub', 'lg96txyrDMmv3Sp0FR5f86GXye9vpCZP')
parameters = pika.ConnectionParameters('cow.rmq2.cloudamqp.com', credentials=credentials, virtual_host='vdfnfbub')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
import json
f = open('data.json')
message = json.load(f)

for i in range(10):
    start=time.time()
    channel.basic_publish(exchange='',
                          routing_key='Input',
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode = 1 # make message persistent
                          ))
    print(time.time()-start)
    time.sleep(2)
