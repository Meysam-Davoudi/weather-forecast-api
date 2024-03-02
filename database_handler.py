import sqlite3


class DatabaseHandler:

    def __init__(self, db_name):
        self.db_name = db_name
        self.__conn = None
        self.create_required_tables()

    def connect(self):
        try:
            self.__conn = sqlite3.connect(self.db_name)
            # print("Connected to database successfully")
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

    def disconnect(self):
        if self.__conn:
            self.__conn.close()
            # print("Disconnected from database")

    def create_required_tables(self):

        query_create_countries_table = """
                CREATE TABLE IF NOT EXISTS countries (
                  id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  capital TEXT NOT NULL,
                  iso2 TEXT NOT NULL,
                  iso3 TEXT NOT NULL
                );
                """

        query_create_request_history_table = """
        CREATE TABLE IF NOT EXISTS `request_history` (
          `id` INTEGER PRIMARY KEY,
          `location` TEXT NOT NULL,
          `lat_lon` TEXT NOT NULL,
          `request_type` TEXT NOT NULL,
          `request_time` TEXT NOT NULL,
          `response` TEXT NOT NULL
        );"""

        self.connect()
        self.execute_query(query_create_countries_table)
        self.execute_query(query_create_request_history_table)
        self.disconnect()

    def select(self, table, columns="*", condition=None):
        try:
            cursor = self.__conn.cursor()
            if condition:
                query = f"SELECT {columns} FROM {table} WHERE {condition}"
            else:
                query = f"SELECT {columns} FROM {table}"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print("Error selecting data:", e)

    def insert(self, table, data):
        # data = {'column_name1': 'value1', 'column_name2': 'value2'}
        try:
            cursor = self.__conn.cursor()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = tuple(data.values())
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            self.__conn.commit()
            # print("Inserted data successfully")
        except sqlite3.Error as e:
            print("Error inserting data:", e)

    def update(self, table, data, condition):
        # data = {'column_name': 'new value'}
        try:
            cursor = self.__conn.cursor()
            set_values = ', '.join([f"{key} = ?" for key in data.keys()])
            values = tuple(data.values())
            query = f"UPDATE {table} SET {set_values} WHERE {condition}"
            cursor.execute(query, values)
            self.__conn.commit()
            # print("Updated data successfully")
        except sqlite3.Error as e:
            print("Error updating data:", e)

    def delete(self, table, condition=None):
        try:
            cursor = self.__conn.cursor()
            query = f"DELETE FROM {table}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            self.__conn.commit()
            # print("Deleted data successfully")
        except sqlite3.Error as e:
            print("Error deleting data:", e)

    def execute_query(self, query):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)
            self.__conn.commit()
            # print("Query executed successfully")
        except sqlite3.Error as e:
            print("Error executing query:", e)
