import sqlite3, logging
from sqlite3 import Error

logging.basicConfig(format="%(asctime)+10s ... %(name)+7s : %(levelname)+9s -> %(message)s",datefmt="%D %I:%M:%S %p", level=logging.NOTSET)
root = logging.getLogger(__file__.split('\\')[-1])
root.propagate = True


class DatabaseManager:
	def __init__(self, db_path:str):

		self.db_path = db_path


	def create_connection(self):
		try:
			connection = sqlite3.connect(self.db_path)
			root.info(f"Successfully connected to {self.db_path}")
		except Error as e:
			root.error(e)
		self.connection = connection


	def close_connection(self):
		if self.connection:
			self.connection.close()
			root.info("Connection Closed.")
		else:
			root.error("No connections found.")



	def execute_query(self, query:str):
		cursor = self.connection.cursor()
		try:
			cursor.execute(query)
			self.connection.commit()
			root.info("Query Successfully executed.")
			return cursor
		except Error as e:
			root.error(e)


	def insert(self, table_name:str, columns, values):
		cursor = self.connection.cursor()
		try:
			cursor.execute(f'INSERT INTO {table_name} {tuple(columns)} VALUES {tuple(values)}')
			self.connection.commit()
			root.info("Value successfully inserted.")
		except Error as e:
			root.error(e)


	def insertmany(self, table_name:str, columns, values_list):
		placeholder = f"({', '.join(tuple('?'*len(values_list[0])))})"
		cursor = self.connection.cursor()
		try:
			cursor.executemany(f"INSERT INTO {table_name} {tuple(columns)} VALUES {placeholder}", values_list)
			self.connection.commit()
			root.info("Values list successfully inserted.")
		except Error as e:
			root.error(e)

	def get_table(self, table_name):
		cursor = self.connection.cursor()
		try:
			# print(cursor.execute(f".schema {table_name}"))
			print('\n\n')

			cursor.execute(f"PRAGMA table_info({table_name})")
			for item in cursor.fetchall():
				print(f"({item[1]} : {item[2]})  ", end=' ')
			print('\n')
			cursor.execute(f"SELECT * FROM {table_name}")
			return (item for item in cursor.fetchall())
		except Error as e:
			root.error(e)
