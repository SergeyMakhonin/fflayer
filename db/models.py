__author__ = 'sergey'

from sqlalchemy import create_engine
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

def create_file_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

def create_schedule_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

