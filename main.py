from deepstack import DeepStackPrediction
from get_image_redis import ImageRedis

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
    print('JSON File:', X.get_json_response())
    print('Number of detected objects:', X.get_no_objects_detected())
    print('All detected objects:', X.get_all_objects_detected())
    print('Dictionary of all detected objects:', X.get_dict_all_objects_detected())

if __name__ == '__main__':
    main()