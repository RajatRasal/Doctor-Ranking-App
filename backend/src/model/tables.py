import os

from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db_connection import get_db_connection

def create_table_if_not_exists(name, db_conn, *cols):
    meta = MetaData(db_conn)
    table = Table(name, meta, *cols)
    res = table.create(db_conn, checkfirst=True)
    return False

def drop_table_if_exists(name, db_conn):
    pass

if __name__ == "__main__":
    # inserting all rows if not exists
    # db_conn = get_db_connection()
    # cols = [Column(Integer, autoincrement=True, primary_key=True)]
    # create_table_if_not_exists('diseases', db_conn, cols)
    pass
