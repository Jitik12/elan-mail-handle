import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


def make_db():
    connection_params = {
        'host': 'localhost',
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
    }
    connection = psycopg2.connect(**connection_params)
    cursor = connection.cursor()
    return connection, cursor
