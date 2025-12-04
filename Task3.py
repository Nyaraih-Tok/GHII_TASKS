import mysql.connector
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee_leave"
    )
def add_month_leave(date_str):
    conn = get_connection()
    cur = conn.cursor()
    d = datetime.strptime(date_str, "%Y-%m-%d")
    year = d.year
    month = d.month