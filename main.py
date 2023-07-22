import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()


HOST_DB = os.getenv('HOST_DB')
PORT_DB = os.getenv('PORT_DB')
USER_DB = os.getenv('USER_DB')
NAME_DB = os.getenv('NAME_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')

def connection():
    try:
        connection = psycopg2.connect(
            host=HOST_DB,
            port=PORT_DB,
            user=USER_DB,
            password=PASSWORD_DB,
            database=NAME_DB
        )
    except Exception as e:
        print('[INFO] Error while connectiong to database ', e)
    return connection




