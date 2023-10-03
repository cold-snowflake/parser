import csv
import sqlite3


class CSVWriter:
    def __init__(self, filename, headers):
        self.filename = filename

        with open(filename, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def write_row(self, data):
        with open(self.filename, 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)


class SQLiteWriter:
    def __init__(self, sql):
        self.sql = sql

        con = sqlite3.connect('car.db')
        cur = con.cursor()

        cur.execute(sql)
        con.commit()
        con.close()

    def commit_sql(self, sql):

        con = sqlite3.connect("car.db")
        cur = con.cursor()

        cur.execute(sql)
        con.commit()
        con.close()
