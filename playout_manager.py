import sys
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.python import log


log.startLogging(sys.stdout)


class SenderFactory(Factory):
    """
    Makes Sender to send commands to playout after we received a request
    """

    def startedConnecting(self, connector):
        sys.stdout.write('Connecting to playout service...')

    def buildProtocol(self, connector):
        sys.stdout.write('Protocol built')
        return Sender()

    def clientConnectionLost(self, connector, reason):
        sys.stdout.write('Lost connection.  Reason: %s' % reason)

    def clientConnectionFailed(self, connector, reason):
        sys.stdout.write('Connection failed. Reason: %s' % reason)


class Sender(Protocol):
    """
    Sends a request to playout service
    """

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)
        if ':confirmed' in data:
            self.transport.loseConnection()

    def connectionMade(self):
        sys.stdout.write('Connected to %s' % self.transport.getHost())
        self.send_request()

    def send_request(self):
        data = b'name,time'
        self.transport.write(data)
        sys.stdout.write('Data sent: %s' % data)


#host = 'localhost'
#port = 8240
#reactor.connectTCP(host, port, SenderFactory())
#reactor.run()


class PlayoutManager:
    def __init__(self, host='localhost', port=8007):
        self.reactor = reactor
        self.reactor.connectTCP(host, port, SenderFactory())

    def run(self):
        self.reactor.run()

    def stop(self):
        self.reactor.callFromThread(reactor.stop)


playout_manager = PlayoutManager(port=8240)
playout_manager.run()