__author__ = 'sergey'

import sys

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import log

from message import Message, convert_received_data
from network_facility import ReceiverFactory

log.startLogging(sys.stdout)


class PlayoutFactory(Factory):
    def buildProtocol(self, addr):
        return Playout()


class Playout(Protocol):
    """
    receives a request for media stream
    """
    def connectionMade(self):
        self.service_name = 'Playout Service'
        sys.stdout.write('{%s connected with host %s' % (self.service_name, self.transport.getHost()))
        try:
            msg = Message(service_role=self.service_name)
            self.transport.write(b'%s', msg.get_byte_string())
        except Exception as e:
            sys.stdout.write('Failed to send role. Reason: %s' % e)

    def connectionLost(self, reason):
        sys.stdout.write('Connection lost: %s' % reason)

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)
        got_msg = convert_received_data(data)
        try:
            msg = Message(confirmed=True, received_data=data)
            self.transport.write(b'%s' % msg.get_byte_string())
        except Exception as e:
            sys.stdout.write('Failed to send confirmation. Reason: %s' % e)


# usage example for Playout 240 (on port 8240)
playout_240 = ReceiverFactory(PlayoutFactory(), 8240)
playout_240.run()
