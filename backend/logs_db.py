import mysql.connector
from datetime import datetime

def get_connection():
    conn = mysql.connector.connect(
        host="mysql",           # Docker service name in docker-compose
        user="root",
        password="mysecure123",
        database="security_logs"
    )
    return conn

def add_log(username, ip, status, message=None):
    """
    Add a log to the database. 'message' is optional.
    """
    conn = get_connection()
    cursor = conn.cursor()
    time_now = datetime.now()
    cursor.execute(
        "INSERT INTO logs (username, ip, status, time, message) VALUES (%s, %s, %s, %s, %s)",
        (username, ip, status, time_now, message)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_logs():
    """
    Fetch all logs, ordered by time descending.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username, ip, status, time, message FROM logs ORDER BY time DESC")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result