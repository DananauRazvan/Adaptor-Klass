import requests
import time
import json
from logs import logs

"""
Send an image to Deepstack object detection API
Returns predictions
"""
class DeepStackPrediction:
    def __init__(self, image_path):
        self.image_data = image_path
        self.dict_object_detected = {}
        self.list_object_detected = []
        self.logs = logs('deepstack.py', 'logs/deepstack_logs')

    def deepstack_response(self):
        try:
            self.logs.info('Deepstack response')

            st = time.time()
            self.response = requests.post('http://localhost:80/v1/vision/detection', files={'image': self.image_data}).json()
            et = time.time()
            self.time = et - st

        except Exception as e:
            self.logs.error('Error occured in Deepstack response ' + str(e))

    def get_no_objects_detected(self):
        return len(self.response['predictions'])

    def get_time_respone(self):
        return self.time

    def get_json_response(self):
        return self.response

    def get_all_objects_detected(self):
        try:
            self.logs.info('All detected objects by Deepstack')

            for object in self.response['predictions']:
                self.list_object_detected.append(object['label'])

            return self.list_object_detected

        except:
            self.logs.error('Error occurred at detection ' + str(e))

    def get_dict_all_objects_detected(self):
        try:
            self.logs.info('Dictionary of all detected objects')

            for object in self.list_object_detected:
                self.dict_object_detected[object] = self.dict_object_detected.get(object, 0) + 1

            return self.dict_object_detected

        except Exception as e:
            self.logs.error('Error occured in dictionary of all detected objects ' + str(e))

    def get_object_det_json_response(self):
        try:
            self.logs.info('JSON response from Deepstack')

            obj_list = []

            for object in self.response['predictions']:
                obj_list.append({'boundingbox': [[object['x_min'], object['y_min']], [object['x_min'], object['y_max']], [object['x_max'], object['y_min']], [object['x_max'], object['y_max']]],
                                 'confidence': int(object['confidence'] * 100),
                                 'label': object['label']})

            message = {
                'OUTPUT': {
                    'PREDICTIONS': [obj_list],
                    'success': self.response['success']
                }
            }

            return message

        except Exception as e:
            self.logs.error('Error occurred in JSON response from Deepstack ' + str(e))
