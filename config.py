import os

# DB related
HOSTNAME = 'e6156.clg4hkuxiisg.us-east-2.rds.amazonaws.com'
PORT = 3306
USERNAME = os.environ.get("DBUSER")
PASSWORD = os.environ.get("DBPW")
DATABASE = 'user_db'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True
