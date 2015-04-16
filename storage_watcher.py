__author__ = 'sergey'

from time import sleep
import os
import sys

from network_facility import ReceiverFactory
from db.processing import DataBase
from db.models import *
from message import Message, convert_received_data

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import log

log.startLogging(sys.stdout)

class StorageWatcher(object):
    def __init__(self, path=None):
        self.storage_files = None
        self.db_files = None
        self.storage_path = None
        self.path = path
        self.need_stashed_files_update = False
        self.db_session = DataBase()
        self.active = True
        self.watch_interval = 5

    def scan_storage(self, path):
        if path: self.path = path
        self.storage_files = os.listdir(self.path)

    def get_stashed_files(self):
        self.db_files = self.session.query(File).all()

    def check_storage_updates(self):

        # Get storage & DB data
        self.scan_storage()
        self.get_stashed_files()

        # Compare storage files & DB files, add missing to DB
        for storage_file in self.storage_files:
            if storage_file in self.db_files:
                self.need_stashed_files_update = False
            else:
                self.need_stashed_files_update = True
                new_file = DataBase.create_object()
                DataBase.add_object(new_file)


class StorageWatcherServiceFactory(Factory):
    def buildProtocol(self, addr):
        return StorageWatcherService()


class StorageWatcherService(Protocol):
    """
    receives start/stop command
    """
    def connectionMade(self):
        self.service_name = 'Storage Watcher Service'
        sys.stdout.write('{%s connected with host %s' % (self.service_name, self.transport.getHost()))
        try:
            msg = Message(service_role=self.service_name)
            self.transport.write(b'%s', msg.get_byte_string())
        except Exception as e:
            sys.stdout.write('Failed to send role. Reason: %s' % e)

    def connectionLost(self, reason):
        sys.stdout.write('%s lost connection with: %s' % (self.service_name, reason))

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)
        got_msg = convert_received_data(data)
        try:
            msg = Message(confirmed=True, received_data=data)
            self.transport.write(b'%s' % msg.get_byte_string())
        except Exception as e:
            sys.stdout.write('Failed to send confirmation. Reason: %s' % e)

        # react on a command
        ## todo code up business logic here
        # start watching

# usage example for StorageWatcherService (on port 8001)
storage_watcher = ReceiverFactory(StorageWatcherService(), 8001)
storage_watcher.run()
