# service.py
import mysql.connector
from mysql.connector import Error


class PointService:
    def __init__(self, host, user, port, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database

    def save_point(self, data):
        try:
            # Establish connection to MySQL database
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                database=self.database
            )

            if connection.is_connected():
                # Define the SQL query
                sql_query = """
                INSERT INTO point (Name, latdegree, latminute, latsecond, longdegree, longminute, longsecond, geodeticheight, h)
                VALUES (%(Name)s, %(latdegree)s, %(latminute)s, %(latsecond)s, %(longdegree)s, %(longminute)s, %(longsecond)s, %(geodeticheight)s, %(h)s)
                """

                # Create a cursor object
                cursor = connection.cursor()

                # Execute the query with the provided data
                cursor.execute(sql_query, data)

                # Commit the transaction
                connection.commit()

                print("Data inserted successfully!")

        except Error as e:
            print("Error while connecting to MySQL", e)

        finally:
            # Close the connection
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

# sql_query = """
#                INSERT INTO your_table (Name, latdegree, latminute, latsecond, longdegree, longminute, longsecond, geodeticheight, h)
#                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#                """

# data not point
# cursor.execute(sql_query, (
#     point.Name, point.latdegree, point.latminute, point.latsecond,
#     point.longdegree, point.longminute, point.longsecond,
#     point.geodeticheight, point.h
# ))
