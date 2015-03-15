__author__ = 'sergey'

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
import db.settings as settings
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

DeclarativeBase = declarative_base()


def connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_schemma(engine):
    """
    creates tables
    """
    DeclarativeBase.metadata.create_all(engine)


class File(DeclarativeBase):
    """
    File table reflects files in file storage
    """
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    duration = Column(Integer)  # in seconds
    parameter = Column(Integer)

    def __repr__(self):
        return "<File(name='%s', time_length='%s')>" % (self.name, self.time_length)


class Schedule(DeclarativeBase):
    """
    File table reflects files in file storage
    """
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_time = Column(Integer)  # in seconds
    duration = Column(Integer)  # in seconds

    def __repr__(self):
        return "<File(name='%s', start_time='%s')>" % (self.name, self.time_length)


class NetworkInfo(DeclarativeBase):
    """
    Stores network info for playout services
    """
    __tablename__ = 'network_info'
    id = Column(Integer, primary_key=True)
    playout_id = Column(String)
    host = Column(String)
    port = Column(String)

    def __repr__(self):
        return "<File(playout_id='%s', host='%s', port='%s')>" % (self.playout_id, self.host, self.port)


# DB connection object
engine = connect()

# create tables
#create_schemma(engine)