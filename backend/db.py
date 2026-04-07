import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"  ✗ Could not connect to database: {e}")
        return None