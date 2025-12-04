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
    
    
    
    
    