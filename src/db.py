import sqlite3

def init_db():
    conn = sqlite3.connect('../data/applications.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS applications
                     (job_id TEXT, company TEXT, email TEXT, status TEXT)''')
    conn.commit()
    return conn, cursor

def check_application(cursor, job_id):
    cursor.execute("SELECT job_id FROM applications WHERE job_id = ?", (job_id,))
    return cursor.fetchone() is not None

def log_application(cursor, conn, job_id, company, email, status):
    cursor.execute("INSERT INTO applications VALUES (?, ?, ?, ?)",
                  (job_id, company, email, status))
    conn.commit()