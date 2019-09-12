"""
Establishing connection to database server.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

def _create_engine_wrapper(url):
    return create_engine(url)

def get_db_connection(drivername='postgres',
                      database=os.environ['PGDATABASE'],
                      port=os.environ['PGPORT'],
                      username=os.environ['PGUSER'],
                      password=os.environ['PGPASSWORD'],
                      host=os.environ['PGHOST']):
    """
    Get sqlalchemy connection engine for database server given connection
    configurations.
    """
    url = URL(**locals())
    return _create_engine_wrapper(str(url))


if __name__ == "__main__":
    print(get_db_connection())
