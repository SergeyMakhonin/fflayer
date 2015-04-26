import sys

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import log

from message import *
from network_facility import ClientFactory, ReceiverFactory

log.startLogging(sys.stdout)


class PlayoutManagerSenderFactory(Factory):
    """
    Makes Sender to send commands to Playout after received a request
    """

    def startedConnecting(self, connector):
        sys.stdout.write('Connecting to playout service...')

    def buildProtocol(self, connector):
        sys.stdout.write('Protocol built')
        return PlayoutManagerSender()

    def clientConnectionLost(self, connector, reason):
        sys.stdout.write('Lost connection.  Reason: %s' % reason)

    def clientConnectionFailed(self, connector, reason):
        sys.stdout.write('Connection failed. Reason: %s' % reason)


class PlayoutManagerSender(Protocol):
    """
    Sends a request to playout service
    """
    def __init__(self):
        Protocol.__init__(self)
        self.service_name = 'Playout Manager Sender Service'

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)
        got_msg = convert_received_data(data)
        confirm(self.transport, got_msg)

    def connectionMade(self):
        std_communication(self.service_name, self.transport)
        
        # send request here
        self.send_request()

    def send_request(self):
        data = b'name,time'

        self.transport.write(data)
        sys.stdout.write('Data sent: %s' % data)


# raw code example
# host = 'localhost'
# port = 8240
# reactor.connectTCP(host, port, SenderFactory())
# reactor.run()


# playout_manager client usage example
# playout_manager = ClientFactory(SenderFactory(), port=8240)
# playout_manager.run()


class PlayoutManagerReceiverFactory(Factory):
    def buildProtocol(self, addr):
        return PlayoutManagerReceiver()


class PlayoutManagerReceiver(Protocol):
    """
    receives a command from database scanner service to pass it to Playout
    """
    def __init__(self):
        Protocol.__init__(self)
        self.service_name = 'Playout Manager Receiver Service'

    def connectionMade(self):
        std_communication(self.service_name, self.transport)

    def connectionLost(self, reason):
        sys.stdout.write('Connection lost: %s' % reason)

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)
        got_msg = convert_received_data(data)
        confirm(self.transport, got_msg)


playout_manager_receiver = ReceiverFactory(PlayoutManagerReceiverFactory(), 8100)