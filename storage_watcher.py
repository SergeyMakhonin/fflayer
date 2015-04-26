import threading

__author__ = 'sergey'

from time import sleep
import os
import sys

from network_facility import *
from db.processing import DataBase
from db.models import *
from message import *

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import log

log.startLogging(sys.stdout)


class StorageWatcher(object, threading.Thread):
    def __init__(self, stop_event, path, interval=None, name='watcher_1'):
        threading.Thread.__init__(name)
        self.storage_files = None
        self.db_files = None
        self.path = path
        self.need_stashed_files_update = False
        self.db_session = DataBase()
        self.active = True
        self.interval = interval
        self.stop_event = stop_event

    def run(self):
        while not self.stop_event.is_set():
            self.watch()

    def scan_storage(self):
        if not self.path:
            return os.listdir(self.path)
        else:
            sys.stdout.write('Path is not set, watcher service will exit.')
            self.stop_event.set()

    def get_stashed_files(self):
        self.db_files = self.db_session.query(File).all()

    def watch(self):

        # Get DB data and add missing to the DB
        while not self.stop_event.is_set():
            if self.storage_files != self.scan_storage():
                self.storage_files = self.scan_storage()
                self.get_stashed_files()

                # Compare storage files & DB files, add missing to DB
                for storage_file in self.storage_files:
                    if storage_file in self.db_files:
                        self.need_stashed_files_update = False
                    else:
                        self.need_stashed_files_update = True
                        new_file = DataBase.create_object('file', name=storage_file,
                                                          path=os.path.join(self.path, storage_file))
                        DataBase.add_object(new_file)
            else:
                sleep(self.interval)


class StorageWatcherServiceFactory(Factory):
    def buildProtocol(self, addr):
        return StorageWatcherService()


class StorageWatcherService(Protocol):
    """
    Receives start/stop command.
    Uses StorageWatcher class for business logic.
    """

    def __init__(self, storage_path):
        Protocol.__init__(self)
        self.service_name = 'Storage Watcher Service'

    def connectionMade(self):
        std_communication(self.service_name, self.transport)

    def connectionLost(self, reason):
        sys.stdout.write('%s lost connection with: %s' % (self.service_name, reason))

    def dataReceived(self, data):
        sys.stdout.write('Data received: %s' % data)
        got_msg = convert_received_data(data)
        confirm(self.transport, got_msg)

        # react on a command
        stop_watcher = threading.Event()
        watcher = StorageWatcher(got_msg.fields['path'])
        watcher.active = got_msg.fields['active']

        # if active - proceed
        if watcher.active:
            if got_msg.fields['interval']:
                watcher.interval = got_msg.fields['interval']
                sys.stdout.write('Watch interval changed to %d' % got_msg.fields['interval'])

            # watch
            watcher.srart()
        else:
            # stop watching if asked
            stop_watcher.set()

# usage example for StorageWatcherService (on port 8001)
path = '/home/Videos'
storage_watcher = ServerFactory(StorageWatcherService(path), 8001)
storage_watcher.run()
