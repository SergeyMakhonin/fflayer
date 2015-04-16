__author__ = 'sergey'

import json

class Message(object):
    def __init__(self, **kwargs):
        self.message = {
            'service_role': kwargs['service_role'],
            'received_data': kwargs['received_data'],
            'confirmed': kwargs['confirmed']
        }

    def get_byte_string(self):
        data = json.dumps(self.message)
        return data

    def set_message_fields(self, d):
        for key, value in d.iteritems():
            if key in self.message:
                self.message.update({key: value})

def convert_received_data(data):
    d = json.loads(data)
    msg = Message().set_message_fields(d)
    return msg