import os

_SETTINGS = {'drivername': 'postgresql',
             'database': os.environ['PGDATABASE'],
             'port': os.environ['PGPORT'],
             'username': os.environ['PGUSER'],
             'password': os.environ['PGPASSWORD'],
             'host': os.environ['PGHOST']}
