import sqlite3

"""
ich bin safe blöd und wenn ich es nicht bin, sqlite. andere DBs um Probleme vorzubeugen


"""

# init interessenten
conn = sqlite3.connect('users_login.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL)''')
conn.commit()
conn.close()
