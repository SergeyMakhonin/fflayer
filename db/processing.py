__author__ = 'sergey'
import pdb
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import db.settings as settings
from db.models import *


class DataBase(object):

    def __init__(self):
        self.connection_made = False
        self.session = None

    def connect(self):
        """
        Performs database connection using database settings from settings.py.
        Returns sqlalchemy engine instance
        Method used to create session object @ create_session_object()
        """
        self.connection_made = True
        return create_engine(URL(**settings.MYSQL))

    def create_session_object(self):
        """
        Create DB connection object & associate it with a Session class to make a session
        Session() object is used for DB transactions
        """
        engine = self.connect()
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_tables(self):
        """
        Create tables (use if no relations exists)
        Does not need a Session()
        """
        engine = self.connect()
        create_schemma(engine)

    def add_object(self, ObjectInstance):
        self.session.add(ObjectInstance)

    @staticmethod
    def create_object(table, **kwargs):
        if table == 'file':
            ObjectInstance = File()
            if 'name' in kwargs:
                ObjectInstance.name = kwargs['name']
            elif 'path' in kwargs:
                ObjectInstance.path = kwargs['path']
            elif 'duration' in kwargs:
                ObjectInstance.duration = kwargs['duration']
            elif 'parameter' in kwargs:
                ObjectInstance.parameter = kwargs['parameter']
            # TODO add field values to ObjectInstance
        elif table == 'schedule':
            ObjectInstance = Schedule()
            if 'name' in kwargs:
                ObjectInstance.name = kwargs['name']
            elif 'start_time' in kwargs:
                ObjectInstance.start_time = kwargs['start_time']
            elif 'duration' in kwargs:
                ObjectInstance.duration = kwargs['duration']
        else:
            raise Exception('Relation is not supported by Watcher Service.')
        return ObjectInstance


DB = DataBase()
DB.create_session_object()
pdb.set_trace()
