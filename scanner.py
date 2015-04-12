__author__ = 'sergey'
import os
from db.processing import DataBase
from db.models import *


class Scanner(object):
    def __init__(self, path=None):
        self.storage_files = None
        self.db_files = None
        self.storage_path = None
        self.path = path
        self.need_stashed_files_update = False
        self.db_session = DataBase()

    def scan_storage(self, path):
        if path: self.path = path
        self.storage_files = os.listdir(self.path)

    def get_stashed_files(self):
        self.db_files = self.session.query(File).all()

    def check_storage_updates(self):

        # Get storage & DB data
        self.scan_storage()
        self.get_stashed_files()

        # Compare storage files & DB files, add missing
        for storage_file in self.storage_files:
            if storage_file in self.db_files:
                self.need_stashed_files_update = False
            else:
                self.need_stashed_files_update = True
                new_file = DataBase.create_object()
                DataBase.add_object(new_file)
