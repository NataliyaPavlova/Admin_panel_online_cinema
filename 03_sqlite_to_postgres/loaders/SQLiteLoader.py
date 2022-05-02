import sqlite3
import sys
from tablesClasses import TABLES, FIELDS, FilmWork#, Person, Genre, PersonFilmWork, GenreFilmWork


class SQLiteLoader:

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def download_data(self, table: str):
        """Download data from SQLite table to array of dataclasses"""
        curs = self.conn.cursor()

        try:
            # read all data from table
            curs.execute("SELECT * FROM {0};".format(table))
            data = curs.fetchall()
            number_of_rows = len(data)

            # parse data to array of dataclasses
            array_dataclasses = []
            class_name = TABLES[table]
            for row in data:
                row_to_insert = (row[field] for field in FIELDS[table])
                dataclass_object = getattr(sys.modules[__name__], class_name)(*row_to_insert)
                array_dataclasses.append(dataclass_object)

            print("Loaded {0} table from SQLite3 database. Number of rows = {1}".format(table, number_of_rows))
            return array_dataclasses
        except (Exception, sqlite3.DatabaseError) as error:
            print("Error: {0}".format(error))
