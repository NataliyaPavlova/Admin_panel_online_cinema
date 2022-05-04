import sqlite3
import sys
import dataclasses
from tablesClasses import TABLES, FilmWork, Person, Genre, PersonFilmWork, GenreFilmWork


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
                dataclass_object = getattr(sys.modules[__name__], class_name)
                fields = dataclass_object.__annotations__.keys()
                row_to_insert = [row[field] for field in fields]
                array_dataclasses.append(dataclass_object(*row_to_insert))

            print("Loaded {0} table from SQLite3 database. Number of rows = {1}".format(table, number_of_rows))
            return array_dataclasses
        except (Exception, sqlite3.DatabaseError) as error:
            print("Error: {0}".format(error))
