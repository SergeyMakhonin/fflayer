__author__ = 'sergey'

import sys
import json

class Message(object):
    def __init__(self, **kwargs):
        self.fields = {
            'service_role': kwargs['service_role'],
            'received_data': kwargs['data'],
            'confirmed': kwargs['confirmed']
        }

    def in_bytes(self):
        data = json.dumps(self.fields)
        return data

    def set_message_fields(self, d):
        for key, value in d.iteritems():
            if key in self.fields:
                self.fields.update({key: value})


def convert_received_data(data):
    d = json.loads(data)
    msg = Message().set_message_fields(d)
    return msg


def std_communication(service_name, transport):
    sys.stdout.write('{%s connected with host %s' % (service_name, transport.getHost()))
    try:
        msg = Message(service_role=service_name)
        transport.write(b'%s', msg.in_bytes())
    except Exception as e:
        sys.stdout.write('Failed to send role. Reason: %s' % e)


def confirm(transport, msg):
    try:
        msg.set_message_fields({'confirmed': True})
        transport.write(b'%s' % msg.received_data.in_bytes())
    except Exception as e:
        sys.stdout.write('Failed to send confirmation. Reason: %s' % e)
