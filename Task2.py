import mysql.connector
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="employee_leave"
    )
    return conn

def get_leave_info(emp_id, start_date, end_date):
   
    conn = get_db_connection()
    cur = conn.cursor()

    # days taken by the employee in this period
    cur.execute("""
        SELECT COALESCE(SUM(leave_days_used), 0)
        FROM LeaveUsage
        WHERE employee_id = %s
          AND exact_leave_date BETWEEN %s AND %s
    """, (emp_id, start_date, end_date))
    taken = cur.fetchone()[0]
    
    # last balance remaining for the employee
    cur.execute("""
        SELECT remaining_leave_days
        FROM LeaveBalance
        WHERE employee_id = %s
        ORDER BY current_date DESC
        LIMIT 1
    """, (emp_id,))
    row = cur.fetchone()
    if row is not None:
        remaining = row[0]
    else:
        remaining = 0

    cur.close()
    conn.close()

    return {
        "taken_days": taken,
        "remaining_days": remaining
    }
    