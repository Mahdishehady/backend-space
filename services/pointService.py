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
                # Create a cursor object
                cursor = connection.cursor()

                # Check if the point already exists
                sql_query_check = """
                SELECT * FROM point WHERE Name = %(Name)s 
                """
                cursor.execute(sql_query_check, data)
                existing_point = cursor.fetchone()

                if existing_point:
                    return "Point already exists"
                else:
                    # Define the SQL query
                    sql_query_insert = """
                    INSERT INTO point (Name, latdegree, latminute, latsecond, longdegree, longminute, longsecond, geodeticheight, h, bs, hdbs, tbs, fs, hdfs, tfs)
                    VALUES (%(Name)s, %(latdegree)s, %(latminute)s, %(latsecond)s, %(longdegree)s, %(longminute)s, %(longsecond)s, %(geodeticheight)s, %(h)s, %(bs)s, %(hdbs)s, %(tbs)s, %(fs)s, %(hdfs)s, %(tfs)s)
                    """
                    # Execute the query with the provided data
                    cursor.execute(sql_query_insert, data)
                    # Commit the transaction
                    connection.commit()
                    return "Data inserted successfully!"

        except Error as e:
            print("Error while connecting to MySQL", e)
            return "Error while connecting to MySQL: {}".format(e)

        finally:
            # Close the connection
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def get_point_details(self, name):
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
                # Create a cursor object
                cursor = connection.cursor()

                # Define the SQL query
                sql_query_select = """
                SELECT Name, bs, hdbs, tbs, fs, hdfs, tfs FROM point WHERE Name = %(Name)s 
                """
                # Execute the query with the provided data
                cursor.execute(sql_query_select, {'Name': name})
                # Fetch the result
                point_details = cursor.fetchone()
                return point_details

        except Error as e:
            print("Error while connecting to MySQL", e)
            return None

        finally:
            # Close the connection
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
