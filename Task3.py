import mysql.connector
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee_leave"
    )