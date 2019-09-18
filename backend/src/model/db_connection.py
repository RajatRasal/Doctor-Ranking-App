"""
Establishing connection to database server.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from src.settings import _SETTINGS

def _create_engine_wrapper(url):
    return create_engine(url)

def get_db_connection(**kwargs):
    """
    Get sqlalchemy connection engine for database server given connection
    configurations.
    """
    if not kwargs:
        kwargs = _SETTINGS

    expected_keys = ['database', 'drivername', 'host', 'password', 'port', 'username']
    for key in expected_keys:
        if key not in kwargs.keys():
            kwargs[key] = _SETTINGS[key]

    url = URL(**kwargs)
    return _create_engine_wrapper(str(url))

if __name__ == "__main__":
    print(get_db_connection())
