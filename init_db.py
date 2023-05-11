import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

create_users = """
	CREATE TABLE IF NOT EXISTS users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT NOT NULL,
		password TEXT NOT NULL,
		last_theme TEXT
	)
"""

cursor.execute(create_users)

connection.commit()

connection.close()