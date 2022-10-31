from deepstack import DeepStackPrediction
from get_image_redis import ImageRedis
from get_data_rabbit import Consumer
from send_json_rabbit import Producer
import pika

def main():
    C = Consumer('vdfnfbub', 'lg96txyrDMmv3Sp0FR5f86GXye9vpCZP')
    C.establish_connection()
    C.call_api_deepstack()
    C.consume()
    C.start_consume()

if __name__ == '__main__':
    main()