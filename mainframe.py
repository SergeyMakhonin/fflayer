__author__ = 'sergey'

import sys

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import log

from message import *
from network_facility import ClientFactory, ServerFactory

log.startLogging(sys.stdout)


class MainFrameSender(Protocol):
    """
    Sends a request to service
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



class MainFrameSenderFactory(Factory):
    """
    Makes Sender to send commands to all services
    """

    def startedConnecting(self, connector):
        sys.stdout.write('Connecting to service...')

    def buildProtocol(self, connector):
        sys.stdout.write('Protocol built')
        return MainFrameSender()

    def clientConnectionLost(self, connector, reason):
        sys.stdout.write('Lost connection.  Reason: %s' % reason)

    def clientConnectionFailed(self, connector, reason):
        sys.stdout.write('Connection failed. Reason: %s' % reason)


class MainFrameReceiverFactory(Factory):
    def buildProtocol(self, addr):
        return MainFrameReceiver()


class MainFrameReceiver(Protocol):
    """
    receives a command from web app or console service to pass it to worker service
    """
    def __init__(self):
        Protocol.__init__(self)
        self.service_name = 'Main Frame Receiver Service'

    def connectionMade(self):
        std_communication(self.service_name, self.transport)

    def connectionLost(self, reason):
        sys.stdout.write('Connection lost: %s' % reason)

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)
        got_msg = convert_received_data(data)
        confirm(self.transport, got_msg)


if __name__ = '__main__':
    mainframe_receiver = MainFrameFactoryReceiver(MainFrameReceiver(), 8001)
