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

    def connect(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print("Error while connecting to MySQL", e)
            return None

    def close_connection(self, connection, cursor):
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    def execute_query(self, cursor, query, data=None):
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print("Error executing SQL query:", e)
            return None

    def save_pair_point(self, pairname):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()

                sql_query_check = """
                SELECT * FROM pairPoints WHERE pairname = %s
                """
                existing_pair_point = self.execute_query(cursor, sql_query_check, (pairname,))

                if existing_pair_point:
                    return "Pair point already exists"
                else:
                    sql_query_insert = """
                    INSERT INTO pairPoints (pairname) VALUES (%s)
                    """
                    cursor.execute(sql_query_insert, (pairname,))
                    connection.commit()
                    return "Pair point inserted successfully!"

        finally:
            self.close_connection(connection, cursor)

    def save_pair_values(self, pair_name: str, point_name: str, data_point: DataPoint):
        try:
            connection = self.connect()
            if connection:
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

        finally:
            self.close_connection(connection, cursor)

    def get_points_by_pairname(self, pairname):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()

                sql_query_select = """
                SELECT pName, BS, HDBS, TBS, FS, HDFS, TFS 
                FROM pairvalues 
                WHERE PairName = %s
                """
                points = self.execute_query(cursor, sql_query_select, (pairname,))
                return points

        finally:
            self.close_connection(connection, cursor)