import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


def get_db_connection(drivername='postgres',
                      database=os.environ['PGDATABASE'],
                      port=os.environ['PGPORT'],
                      username=os.environ['PGUSER'],
                      password=os.environ['PGPASSWORD'],
                      host=os.environ['PGHOST']):
    return create_engine(URL(**locals()))


if __name__ == "__main__":
    print(get_db_connection())
