"""
Tests for the doctor ranking algorithm.
"""
import mock
import pytest
import sqlalchemy

from src.db import db_connection

"""
mock.patch('sqlalchemy.create_engine')
def test_connection_formation(mock_create_engine):
    drivername = 'postgres'
    host = 'localhost'
    port = '5432'
    SETTINGS = {
        'drivername': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': 'username',
        'password': 'password',
        'database': 'db_name'
    }
    url = f"{SETTINGS['drivername']
    mock_create_engine.assert_called_once_with(
    db_connection(SETTINGS)
"""
