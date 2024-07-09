import sqlite3

def setup_database():
    conn = sqlite3.connect('results.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (id INTEGER PRIMARY KEY, result_json TEXT, latitude REAL, longitude REAL)''')
    conn.commit()
    conn.close()

setup_database()

