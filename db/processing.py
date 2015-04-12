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
        return create_engine(URL(**settings.DATABASE))

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

    def create_object(self, table, **kwargs):
        if table == 'file':
            ObjectInstance = File()
            if 'name' in kwargs:
                ObjectInstance.name = kwargs['name']
            elif 'duration' in kwargs:
                ObjectInstance.duration = kwargs['duration']
            elif 'parameter' in kwargs:
                ObjectInstance.parameter = kwargs['parameter']
            # TODO add field values to ObjectInstance
        elif table == 'schedule': pass
        else:
            raise Exception('Relation does not exist.')
        return ObjectInstance


#DB = DataBase()
#DB.create_session_object()
#pdb.set_trace()
