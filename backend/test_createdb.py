import os

from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


user = os.environ['PGUSER']
password = os.environ['PGPASSWORD']
host = os.environ['PGHOST']
port = os.environ['PGPORT']
database = os.environ['PGDATABASE']

db_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'

print(db_string)
db = create_engine(db_string)

base = declarative_base()

class Diseases(base):
    __tablename__ = 'diseases'

    disease_id = Column(Integer, autoincrement=True, primary_key=True)
    disease_type = Column(String)

Session = sessionmaker(db)
session = Session()

print("HERE")
base.metadata.create_all(db)
print("HERE")
disease_oncology = Diseases(disease_type="oncology")
disease_haematology = Diseases(disease_type='haematology')
session.add(disease_oncology)
session.add(disease_haematology)
session.commit()

"""
with db.connect() as conn:
    res = db.execute("select table_name, column_name from information_schema.columns where table_name='diseases'")
    for row in res:
        print(row)

print('here')

def main():
    import psycopg2 as db
    try:
        conn = db.connect(host="localhost", database="doctor_rank", port="5432",
                          user="postgres", password="thisisforpostgres")
        print('Connected')

        cursor = conn.cursor()
        cursor.execute("select table_name, column_name from information_schema.columns where table_name='diseases'")

        for row in cursor.fetchall():
            print(row)

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

main()
"""
