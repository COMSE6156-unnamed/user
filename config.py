import os
from sqlalchemy import create_engine

# DB related
HOSTNAME = 'e6156.ccgom5f9kwrf.us-east-1.rds.amazonaws.com'
PORT = 3306
USERNAME = os.environ.get("DBUSER")
PASSWORD = os.environ.get("DBPW")
DATABASE = 'user_db'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

def create_db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    return engine