import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="mysql",           # service name in docker-compose
        user="root",
        password="mysecure123", # <- use the same password here
        database="security_logs"
    )
    return conn

def add_log(message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (message) VALUES (%s)", (message,))
    conn.commit()
    cursor.close()
    conn.close()

def get_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result