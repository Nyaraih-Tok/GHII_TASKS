import mysql.connector
from datetime import datetime

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee_leave"
    )
    return conn

def add_month_leave(date_str):
    conn = get_connection()
    cur = conn.cursor()

    d = datetime.strptime(date_str, "%Y-%m-%d")
    year = d.year
    month = d.month
   
    cur.execute("SELECT employee_id, date_of_entry FROM Employee")
    employee_list = cur.fetchall()

    for emp_id, date_of_entry in employee_list:
        
        hire_date = datetime.strptime(str(date_of_entry), "%Y-%m-%d")

        first_of_month = datetime(year, month, 1)
      #checking if the employee joined in the middle of the month 
        
        if hire_date > first_of_month:
            continue

        
        cur.execute("""
            INSERT INTO LeaveEntitlement
                (employee_id, accumulated_days, entitled_days,
                 months_worked, period_year, period_month)
            VALUES (%s, 1.25, 1.25, 1, %s, %s)
        """, (emp_id, year, month))

        
        cur.execute("""
            SELECT COALESCE(SUM(entitled_days + accumulated_days), 0)
            FROM LeaveEntitlement
            WHERE employee_id = %s
        """, (emp_id,))
        total_entitled = cur.fetchone()[0]

        
        cur.execute("""
            SELECT COALESCE(SUM(leave_days_used), 0)
            FROM LeaveUsage
            WHERE employee_id = %s
        """, (emp_id,))
        total_used = cur.fetchone()[0]

        
        remaining = total_entitled - total_used

       
        if month == 12:
            remaining = remaining * 0.5

    #inserting the new balance
        cur.execute("""
            INSERT INTO LeaveBalance
                (employee_id, total_balance, remaining_leave_days, current_date)
            VALUES (%s, %s, %s, %s)
        """, (emp_id, total_entitled, remaining, date_str))

    conn.commit()
    cur.close()
    conn.close()
