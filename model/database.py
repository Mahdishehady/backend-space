import mysql.connector


class Database:
    def __init__(self, host, user, port, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            database=self.database
        )

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def execute_insert(self, query, data):
        cursor = self.connection.cursor()
        cursor.execute(query, data)
        self.connection.commit()
