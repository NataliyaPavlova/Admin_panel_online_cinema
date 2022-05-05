"""Migrate data from SQLite db to Postgres db"""
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager
import sys
import os

from config import db
from loaders.SQLiteLoader import SQLiteLoader
from loaders.PostgresLoader import PostgresLoader
from tablesClasses import TABLES

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from tests.check_consistency.tests import Tests


@contextmanager
def conn_context(db_path: str):
    """Context manager for sqlite connection"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def main():
    """Main module for data migration"""
    batch_size = 500
    dsl = db.DATABASES['postgres']

    with conn_context(db.DATABASES['sqlite']['dbname']) as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        sqlite_loader = SQLiteLoader(sqlite_conn)
        postgres_loader = PostgresLoader(pg_conn)
        test = Tests(sqlite_conn, pg_conn)
        for table in TABLES.keys():
            data = sqlite_loader.download_data(table)
            postgres_loader.upload_data(table, data, batch_size)
            test.check_count(table)
            test.check_values(table)


if __name__ == '__main__':
    main()
