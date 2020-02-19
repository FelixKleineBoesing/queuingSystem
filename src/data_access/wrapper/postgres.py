import psycopg2
from psycopg2 import sql
from psycopg2.sql import SQL, Identifier, Placeholder
import logging
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

    def get_table(self, table_name: str, columns: list = None, where_condition: list = None, group: list = None):
        """

        :param table_name: name of the postgres table
        :param columns: list of strings or dictionaries. if group is not None this must be a list of dictionaries
            containing each at least the keys "column" and "func". "func" contains the aggregaction function by which the
            specified column should be aggregated. You are able to specify a new name of this column with the key "new_name"
        :param where_condition: where condition for the selected columns
        :param group: list of column by which the table should be grouped

        :return:
        """
        if columns is not None:
            assert isinstance(columns, list)
            if group is None:
                assert all([isinstance(col, str) for col in columns])
            else:
                assert all([isinstance(col, dict) for col in columns])
                assert all([all([key in agg_col for key in ["column", "func"]]) for agg_col in columns])

        if columns is None:
            string = "SELECT * "
            sql_objects = []
        else:
            string = "SELECT {}"
            if group is None:
                cols = sql.SQL(",").join(map(sql.Identifier, columns))
                sql_objects = [cols]
            else:
                sql_objects = [sql.SQL(",").join(map(sql.Identifier, group))]
                for i, col in enumerate(columns):
                    if "new_name" not in col:
                        name = "{}_{}".format(col["func"], col["column"])
                    else:
                        name = col["new_name"]
                    string += ", {}({}) AS {}".format(col["func"], "{}", name)
                    sql_objects.append(sql.Identifier(col["column"]))

        string += " FROM {}"
        sql_objects.append(sql.Identifier(table_name))

        if where_condition is not None:
            string += " WHERE " + " and ".join(["{} {} {}".format("{}", cond["condition"], "{}")
                                                for cond in where_condition])
            for item in where_condition:
                sql_objects.extend([sql.Identifier(item["column"]), sql.Placeholder()])
            values = [cond["value"] for cond in where_condition]
        else:
            values = None

        if group is not None:
            string += " GROUP BY {}"
            sql_objects.append(sql.SQL(",").join(map(sql.Identifier, group)))

        sql_string = sql.SQL(string).format(*sql_objects)

        table = self.get_query(query=sql_string, fetch=True, values=values)
        if len(table) > 0:
            column_names = self.get_column_names(table_name=table_name)
            data = pd.DataFrame(table, columns=column_names)
        else:
            data = pd.DataFrame(table)
        return data

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

    def insert_from_df(self, df: pd.DataFrame, table: str, page_size: int = 1000, commit: bool = False,
                       on_conflict: str = None, id_cols: list = None, update_cols: list = None):
        assert (isinstance(df, pd.DataFrame))
        assert (isinstance(table, str))
        assert (isinstance(page_size, int))
        assert (isinstance(commit, bool))
        assert (on_conflict in ["do_nothing", "do_update", None])
        assert (isinstance(id_cols, (list, type(None))))
        assert (isinstance(update_cols, (list, type(None))))

        df.replace(to_replace=[float('nan')], value=[None], inplace=True)
        df_columns = list(df)
        columns = (', '.join('"' + col + '"' for col in df_columns))
        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
        insert_stmt = "INSERT INTO {} ({}) {}".format(table, columns, values)

        # add "on conflict" statement
        if on_conflict == "do_nothing":
            if id_cols is None:
                insert_stmt = "{} ON CONFLICT DO NOTHING".format(insert_stmt)
            else:
                insert_stmt = "{} ON CONFLICT ({}) DO NOTHING".format(insert_stmt,
                                                                      (', '.join('"' + col + '"' for col in id_cols)))
        elif on_conflict == "do_update":
            if update_cols is None:
                update_cols = columns
            update_stmt = "{} ON CONFLICT({}) DO UPDATE SET ({}) = ({})" if len(update_cols) > 1 \
                else "{} ON CONFLICT({}) DO UPDATE SET {} = {}"
            insert_stmt = update_stmt.format(insert_stmt,
                                             (', '.join('"' + col + '"' for col in id_cols)),
                                             (', '.join('"' + col + '"' for col in update_cols)),
                                             (', '.join('EXCLUDED."' + col + '"' for col in update_cols)))
        logging.debug("Upsert rows ...") if on_conflict == "do_update" else logging.debug("Insert rows ...")
        with psycopg2.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            psycopg2.extras.execute_batch(cursor, insert_stmt, df.values, page_size=page_size)
        if commit:
            conn.commit()
            logging.debug("Data succesfully inserted.")
