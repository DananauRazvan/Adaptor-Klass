from deepstack import DeepStackPrediction
from get_image_redis import ImageRedis
from get_data_rabbit import Consumer
from send_json_rabbit import Producer
import pika

def main():
    X = ImageRedis('localhost', '6379', 'test_images/test_image.jpg')
    X.establish_connection()
    X.read_image()
    X.encode_image()
    X.write_redis()
    X.read_from_redis()
    encoded_message = X.get_encoded_image() # Encoded message read from Redis

    X = DeepStackPrediction(encoded_message)
    X.deepstack_response()
    # print('JSON File:', X.get_json_response())
    # print('Number of detected objects:', X.get_no_objects_detected())
    # print('All detected objects:', X.get_all_objects_detected())
    # print('Dictionary of all detected objects:', X.get_dict_all_objects_detected())
    # print('JSON message:', X.get_object_det_json_response())
    if X.get_no_objects_detected() > 0:
        C = Consumer('vdfnfbub', 'lg96txyrDMmv3Sp0FR5f86GXye9vpCZP', X.get_object_det_json_response())

    else:
        C = Consumer('vdfnfbub', 'lg96txyrDMmv3Sp0FR5f86GXye9vpCZP', '')

    C.establish_connection()
    C.consume()
    C.start_consume()
if __name__ == '__main__':
    main()