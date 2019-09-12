import os

from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db_connection import get_db_connection


base = declarative_base()

"""
class Diseases(base):
    __tablename__ = 'diseases'

    disease_id = Column(Integer, autoincrement=True, primary_key=True)
    disease_type = Column(String)

class Parameters(base):
    __tablename__ = 'parameters'

    parameter_id = Column(Integer, autoincrement=True, primary_key=True)
    parameter_type = Column(String)

class Doctors(base):
    __tablename__ = 'doctors'

    doctor_id = Column(Integer, autoincrement=True, primary_key=True)
    firstname = ''
    surname = ''
    w1 = ''
    w2 = ''
"""

def create_table_if_not_exists(name, db_conn, *cols):
    return True

def drop_table_if_exists(name, db_conn):
    pass


# Session = sessionmaker(db)
# session = Session()
# 
# db = create_engine(db_string)
# print("HERE")
# base.metadata.create_all(db)
# print("HERE")
# disease_oncology = Diseases(disease_type="oncology")
# disease_haematology = Diseases(disease_type='haematology')
# session.add(disease_oncology)
# session.add(disease_haematology)
# session.commit()

if __name__ == "__main__":
    # inserting all rows if not exists
    db_conn = get_db_connection()
    cols = [Column(Integer, autoincrement=True, primary_key=True)]
    create_table_if_not_exists('diseases', db_conn, cols)
