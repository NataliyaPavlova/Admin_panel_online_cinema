import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import contextmanager

from config import db
from loaders.SQLiteLoader import SQLiteLoader
from loaders.PostgresLoader import PostgresLoader
from tablesClasses import TABLES, FilmWork#, Person, Genre, PersonFilmWork, GenreFilmWork


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def main():
    batch_size = 500
    dsl = db.DATABASES['postgres']

    with conn_context(db.DATABASES['sqlite']['dbname']) as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        sqlite_loader = SQLiteLoader(sqlite_conn)
        postgres_loader = PostgresLoader(pg_conn)
        for table in TABLES.keys(): #, Person, Genre, Person_film_work, Genre_film_work]:
            data = sqlite_loader.download_data(table)
            postgres_loader.upload_data(table, data, batch_size)


if __name__ == '__main__':
    main()

