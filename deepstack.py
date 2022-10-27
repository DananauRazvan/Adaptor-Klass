import requests
import time


"""
Send an image to Deepstack object detection API
Returns predictions
"""
class DeepStackPrediction:
    def __init__(self, image_path):
        self.image_data = image_path
        self.dict_object_detected = {}
        self.list_object_detected = []

    def deepstack_response(self):
        st = time.time()
        self.response = requests.post('http://localhost:80/v1/vision/detection', files={'image': self.image_data}).json()
        et = time.time()
        self.time = et - st

    def get_no_objects_detected(self):
        return len(self.response['predictions'])

    def get_time_respone(self):
        return self.time

    def get_json_response(self):
        return self.response

    def get_all_objects_detected(self):
        for object in self.response['predictions']:
            self.list_object_detected.append(object['label'])
            # self.list_object_detected[object] = self.list_object_detected.get(object, 0) + 1 .append(object['label'])

        return self.list_object_detected

    def get_dict_all_objects_detected(self):
        for object in self.list_object_detected:
            self.dict_object_detected[object] = self.dict_object_detected.get(object, 0) + 1

        return self.dict_object_detected