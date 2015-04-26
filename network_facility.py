__author__ = 'sergey'

import sys

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import log

from message import *

log.startLogging(sys.stdout)


class ServerFactory:
    """
    initializes a server to process data using given protocol_factory
    """

    def __init__(self, protocol_factory, port=8007):
        self.endpoint = TCP4ServerEndpoint(reactor, port)
        self.endpoint.listen(protocol_factory)
        self.reactor = reactor

    def run(self):
        self.reactor.run()

    def stop(self):
        self.reactor.callFromThread(reactor.stop)


class ClientFactory:
    """
    initializes client to send data using given protocol_factory
    """
    def __init__(self, protocol_factory, host='localhost', port=8003):
        self.reactor = reactor
        self.reactor.connectTCP(host, port, protocol_factory)

    def run(self):
        self.reactor.run()

    def stop(self):
        self.reactor.callFromThread(reactor.stop)
