__author__ = 'sergey'

import sys
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.python import log


log.startLogging(sys.stdout)


class ReceiverFactory(Factory):
    def buildProtocol(self, addr):
        return Receiver()


class Receiver(Protocol):
    """
    receives a request for media stream
    """
    def connectionMade(self):
        sys.stdout.write('Connection made')

    def connectionLost(self, reason):
        sys.stdout.write('Connection lost: %s' % reason)

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)


class PlayoutFactory:
    """
    hosts playout server and delivers instructions to stream.py
    """
    def __init__(self, protocol_factory, port=8007):
        self.endpoint = TCP4ServerEndpoint(reactor, port)
        self.endpoint.listen(protocol_factory)
        self.reactor = reactor
    def run(self):
        self.reactor.run()
    def stop(self):
        self.reactor.callFromThread(reactor.stop)


# usage example
playout_240 = PlayoutFactory(ReceiverFactory(), 8007)
