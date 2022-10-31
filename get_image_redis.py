import redis
import cv2
import numpy as np
from logs import logs

"""
Get image from Redis
"""
class ImageRedis:
    def __init__(self, host, port, image_path):
        self.host = host
        self.port = port
        self.image_path = image_path
        self.logs = logs('get_image_redis.py', 'logs/get_image_redis_logs')

    def establish_connection(self):
        self.redis = redis.Redis(host=self.host, port=self.port)

    def read_image(self):
        self.image = cv2.imread(self.image_path)

    def encode_image(self):
        _, buffer = cv2.imencode(self.image_path[-4:], self.image)
        self.image_bytes = np.array(buffer).tobytes()

    def write_redis(self):
        self.redis.set(self.image_path, self.image_bytes)

    def read_from_redis(self):
        self.read_redis = self.redis.get(self.image_path)

    def get_encoded_image(self):
        try:
            self.logs.info('Get image from Redis')

            return self.read_redis

        except Exception as e:
            self.logs.error('Error occurred in Redis ' + str(e))