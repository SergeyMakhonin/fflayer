__author__ = 'sergey'
import os
from db.processing import DataBase
from db.models import *

class Scanner(object):
    def __init__(self):
        self.db_session = DataBase()
        self.storage_files
        self.db_data

    def scan_storage(self, path):
        self.storage_files = os.listdir(path)

    def scan_database(self):
        self.db_data = self.db_session.session.query(File)