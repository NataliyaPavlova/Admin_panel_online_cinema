import sqlite3
from psycopg2.extensions import connection as _connection


class Tests:

    def __init__(self, sqlite_connection: sqlite3.Connection, pg_connection: _connection):
        self.sqlite_conn = sqlite_connection
        self.sqlite_cur = self.sqlite_conn.cursor()
        self.pg_conn = pg_connection
        self.pg_cur = self.pg_conn.cursor()

    def check_count(self, table):
        stmt = "select count(*) as cnt from {0};".format(table)
        sqlite_row = self.sqlite_cur.execute(stmt).fetchone()
        sqlite_count = dict(sqlite_row)
        pg_stmt = "select count(*) from content.{0}".format(table)
        self.pg_cur.execute(pg_stmt)
        pg_count = dict(self.pg_cur.fetchone())
        assert sqlite_count['cnt'] == pg_count['count']

    def check_values(self, table):
        sqlite_stmt = "select * from {0};".format(table)
        sqlite_select = self.sqlite_cur.execute(sqlite_stmt).fetchall()
        for row in sqlite_select:
            sql_dict = dict(row)
            sql_dict.pop('created_at', None)
            sql_dict.pop('updated_at', None)
            pg_stmt = "select * from content.{0} where id='{1}'".format(table, row['id'])
            self.pg_cur.execute(pg_stmt)
            pg_row = self.pg_cur.fetchone()
            pg_dict = dict(pg_row)
            pg_dict.pop('created_at', None)
            pg_dict.pop('updated_at', None)
            assert sql_dict == pg_dict

