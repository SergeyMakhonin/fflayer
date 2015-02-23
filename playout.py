__author__ = 'sergey'

import sys
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import log
from facility import ReceiverFactory

log.startLogging(sys.stdout)


class PlayoutFactory(Factory):
    def buildProtocol(self, addr):
        return Playout()


class Playout(Protocol):
    """
    receives a request for media stream
    """

    def connectionMade(self):
        sys.stdout.write('Connection made with host %s' % self.transport.getHost())

    def connectionLost(self, reason):
        sys.stdout.write('Connection lost: %s' % reason)

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)
        try:
            self.transport.write(data + b' :confirmed')
        except Exception as e:
            sys.stdout.write('Failed to send confirmation. Reason: %s' % e)

# usage example for Playout 240 (on port 8240)
playout_240 = ReceiverFactory(PlayoutFactory(), 8240)
playout_240.run()
