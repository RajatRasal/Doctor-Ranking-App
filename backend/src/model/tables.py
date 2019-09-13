"""
ORM functions for creating and deleting table definitions in the database, 
equivalent to DDL only using SQLAlchemy's ORM instead of SQL.
"""
import os

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column,\
    ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db_connection import get_db_connection

def create_table_if_not_exists(name, db_conn, *cols):
    meta = MetaData(db_conn)
    meta.reflect()
    try:
        table = Table(name, meta, *cols)
        table.create(db_conn, checkfirst=True)
        return table
    except sqlalchemy.exc.InvalidRequestError:
        return None

def drop_table_if_exists(name, db_conn):
    pass

if __name__ == "__main__":
    db_conn = get_db_connection()

    diseases = create_table_if_not_exists('diseases', db_conn, 
        Column('id', Integer, primary_key=True),
        Column('type', String))

    parameters = create_table_if_not_exists('parameters', db_conn, 
        Column('id', Integer, primary_key=True),
        Column('type', String))

    dis_param_link_name = 'disease_params_importance' 
    disease_params_importance = create_table_if_not_exists(dis_param_link_name,
        db_conn,
        Column('disease_id', Integer, ForeignKey('diseases.id'), nullable=False),
        Column('parameter_id', Integer, ForeignKey('parameters.id'),
               nullable=False),
        Column('importance', Integer, nullable=False))

    inspector = inspect(db_conn.connect())
    print(f'Existing tables: {inspector.get_table_names()}')
