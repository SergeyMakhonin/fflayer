__author__ = 'sergey'
import pdb
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import db.settings as settings
from db.models import *


# Function used to create session object @ create_session_object()
def connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


# Create DB connection object & associate it with a Session class to make a session
def create_session_object():
    """
    Returns session = Session() object that is used for DB transactions
    :return: Session
    """
    engine = connect()
    Session = sessionmaker(bind=engine)
    return Session()


# Create tables
def create_tables():
    engine = connect()
    create_schemma(engine)

# session = create_session_object()
# pdb.set_trace()
