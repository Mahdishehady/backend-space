import mysql.connector
from mysql.connector import Error


class PointService:
    def __init__(self, host, user, port, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database

    def _connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            database=self.database
        )

    def save_point(self, data):
        try:
            connection = self._connect()

            if connection.is_connected():
                cursor = connection.cursor()

                sql_query_check = """
                SELECT * FROM point WHERE Name = %(Name)s 
                """
                cursor.execute(sql_query_check, data)
                existing_point = cursor.fetchone()

                if existing_point:
                    return "Point already exists"
                else:
                    sql_query_insert = """
                    INSERT INTO point (Name, latdegree, latminute, latsecond, longdegree, longminute, longsecond, geodeticheight, h)
                    VALUES (%(Name)s, %(latdegree)s, %(latminute)s, %(latsecond)s, %(longdegree)s, %(longminute)s, %(longsecond)s, %(geodeticheight)s, %(h)s)
                    """
                    cursor.execute(sql_query_insert, data)
                    connection.commit()
                    return "Data inserted successfully!"

        except Error as e:
            print("Error while connecting to MySQL", e)
            return "Error while connecting to MySQL: {}".format(e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def get_all_points(self):
        try:
            connection = self._connect()

            if connection.is_connected():
                cursor = connection.cursor()

                sql_query_get_all_points = """
                SELECT * FROM point
                """
                cursor.execute(sql_query_get_all_points)
                all_points = cursor.fetchall()
                return all_points

        except Error as e:
            print("Error while connecting to MySQL", e)
            return "Error while connecting to MySQL: {}".format(e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
