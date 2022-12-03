import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

# DB related
HOSTNAME = os.environ.get("RDS_HOSTNAME")
PORT = os.environ.get("RDS_PORT")
USERNAME = os.environ.get("DBUSER")
PASSWORD = os.environ.get("DBPW")
DATABASE = 'user_db'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

def create_db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    return engine