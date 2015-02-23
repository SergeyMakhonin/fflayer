__author__ = 'sergey'

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint


class ReceiverFactory:
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
    def __init__(self, protocol_factory, host='localhost', port=8007):
        self.reactor = reactor
        self.reactor.connectTCP(host, port, protocol_factory)

    def run(self):
        self.reactor.run()

    def stop(self):
        self.reactor.callFromThread(reactor.stop)
