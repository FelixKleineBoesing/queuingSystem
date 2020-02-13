import psycopg2
from psycopg2.sql import SQL, Identifier
import sqlalchemy
from typing import Union
import pandas as pd


class PostgresWrapper:

    __instance = None

    def __init__(self, host: str, port: int, user: str, password: str, dbname: str):
        if self.__class__.__instance is None:
            self.host = host
            self.port = port
            self.user = user
            self.password = password
            self.dbname = dbname
            self.connection_string = "dbname='{}' user='{}' host='{}' password='{}' port='{}'".\
                format(dbname, user, host, password, port)
            self.__class__.__instance = self
        else:
            raise ValueError("This class is a singleton and already initialised. Get instance instead!")

    @classmethod
    def get_instance(cls):
        """
        returns the instance of this Wrapper if there is one, otherwise raises ValueError

        :return:
        """
        if cls.__instance is None:
            raise ValueError("This Wrapper must be initialised first!")
        return cls.__instance

    def get_column_names(self, table_name: str = None, cursor=None):
        """
        either supply a table_name or a cursor from a query

        :param table_name:
        :param cursor:
        :return:
        """
        assert table_name is not None or cursor is not None
        if table_name is not None:
            cursor = self.get_query("SELECT * from {} LIMIT 1;".format(table_name))

        desc = cursor.description()
        column_names = [des[0] for des in desc]
        return column_names

    def get_table(self, table_name: str, columns: list = None, condition: str = None):
        """
        execute a query for the specified table and considers the conditions

        :param table_name: name of the postgres table from which the data should be retrieved
        :param condition: condition in string format ( e.g, where NUMBER >= 10
        :return: the table as a dataframe
        """
        if columns is None:
            query = SQL("SELECT * from")
        else:
            query = SQL("SELECT {} from").format(SQL(", ").join(map(Identifier, columns)))
        query += SQL(" {}").format(Identifier(table_name))
        # TODO add conditions
        table = self.get_query(query)
        column_names = self.get_column_names()
        return pd.DataFrame(table, columns=column_names)

    def get_query(self, query: Union[SQL, str], fetch: bool = True):
        """
        send a generic query and fetch the results

        :param query: SQL query string
        :param fetch: whether to fetch or not inside this function
        :return: depending on the fetch argument
        """
        if isinstance(query, str):
            query = SQL(query)
        with psycopg2.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query.as_string(cursor))
            if fetch:
                return cursor.fetchall()
            else:
                return cursor
