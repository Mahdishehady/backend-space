from typing import Dict

import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
class DataPoint(BaseModel):
    bs: str
    hdbs: str
    tbs: str
    fs: str
    hdfs: str
    tfs: str

class pairPointService:
    def __init__(self, host, user, port, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database

    def save_pair_point(self, pairname):
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

                # Check if the pair point already exists
                sql_query_check = """
                SELECT * FROM pairPoints WHERE pairname = %s
                """
                cursor.execute(sql_query_check, (pairname,))
                existing_pair_point = cursor.fetchone()

                if existing_pair_point:
                    return "Pair point already exists"
                else:
                    # Define the SQL query
                    sql_query_insert = """
                    INSERT INTO pairPoints (pairname) VALUES (%s)
                    """
                    # Execute the query with the provided data
                    cursor.execute(sql_query_insert, (pairname,))
                    # Commit the transaction
                    connection.commit()
                    return "Pair point inserted successfully!"

        except Error as e:
            print("Error while connecting to MySQL", e)
            return "Error while connecting to MySQL: {}".format(e)

        finally:
            # Close the connection
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def save_pair_values(self, pair_name: str, point_name: str, data_point: DataPoint):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                database=self.database
            )

            if connection.is_connected():
                cursor = connection.cursor()

                sql_query_insert = """
                INSERT INTO pairValues (PairName, pName, BS, HDBS, TBS, FS, HDFS, TFS)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (pair_name, point_name, float(data_point.bs), float(data_point.hdbs),
                          float(data_point.tbs), float(data_point.fs), float(data_point.hdfs),
                          float(data_point.tfs))
                cursor.execute(sql_query_insert, values)

                connection.commit()
                return "Point inserted successfully!"

        except Error as e:
            print("Error while connecting to MySQL", e)
            return "Error while connecting to MySQL: {}".format(e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")