__author__ = 'sergey'

import sys

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import log

from message import *
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
        std_communication(self.service_name, self.transport)

    def connectionLost(self, reason):
        sys.stdout.write('Connection lost: %s' % reason)

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)
        got_msg = convert_received_data(data)
        confirm(self.transport, got_msg)


# usage example for Playout 240 (on port 8240)
playout_240 = ReceiverFactory(PlayoutFactory(), 8240)
playout_240.run()
