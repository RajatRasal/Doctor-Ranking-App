"""
Tests for establishing connections to database servers.
"""
import os

import mock
import pytest

class TestDatabaseConnection:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """
        Setup postgres connection environment variables.
        """

        print('SETUP-----------------------------------------')

    @mock.patch('src.model.db_connection._create_engine_wrapper')
    def test_default_connection_to_postgres(self, mock_create_engine):
        """
        Tests that URL for connection to postgres db is formed correctly and
        passed into sqlalchemy Engine object without any inputs.
        """
        from src.model.db_connection import get_db_connection

        # Expected values
        db = os.environ['PGDATABASE']
        port = os.environ['PGPORT']
        user = os.environ['PGUSER']
        pwd = os.environ['PGPASSWORD']
        host = os.environ['PGHOST']

        # Mock out return value of _create_engine_wrapper
        expected_test_connection = "Engine connection"
        mock_create_engine.return_value = expected_test_connection

        test_connection = get_db_connection()

        # Test call to wrapper
        url = f'postgresql://{user}:{pwd}@{host}:{port}/{db}'
        mock_create_engine.assert_called_once_with(url)

        # Test that the postgres connection engine is being returned directly
        # without any further changes to it.
        assert test_connection == mock_create_engine.return_value

    @mock.patch('src.model.db_connection._create_engine_wrapper')
    def test_default_connection_to_postgres(self, mock_create_engine):
        """
        Tests that URL for connection to postgres db is formed correctly and
        passed into sqlalchemy Engine object.
        """
        from src.model.db_connection import get_db_connection

        drivername = 'test_driver'
        db = 'test_db'
        port = '1234' 
        user = 'test_user' 
        pwd = 'test_password' 
        host = 'test_host' 

        expected_test_connection = "Engine connection"
        mock_create_engine.return_value = expected_test_connection

        test_connection = get_db_connection(database=db, drivername=drivername,
                                            username=user, password=pwd,
                                            host=host, port=port)

        url = f'postgresql://{user}:{pwd}@{host}:{port}/{db}'
        mock_create_engine.assert_called_once_with(url)

        assert test_connection == mock_create_engine.return_value

    @mock.patch('src.model.db_connection._create_engine_wrapper')
    @pytest.mark.parametrize('key', ['drivername', 'database', 'port',
                                     'username', 'password', 'host'])
    def test_default_connection_to_postgres(self, mock_create_engine, key):
        """
        Tests that URL for connection to postgres db is formed correctly and
        passed into sqlalchemy Engine object when only partial spec is given.
        """
        from src.model.db_connection import get_db_connection

        _SETTINGS = {'drivername': 'postgresql',
                     'database': os.environ['PGDATABASE'],
                     'port': os.environ['PGPORT'],
                     'username': os.environ['PGUSER'],
                     'password': os.environ['PGPASSWORD'],
                     'host': os.environ['PGHOST']}
        
        url = f'{_SETTINGS["drivername"]}://{_SETTINGS["username"]}:{_SETTINGS["password"]}@{_SETTINGS["host"]}:{_SETTINGS["port"]}/{_SETTINGS["database"]}'

        del _SETTINGS[key]

        expected_test_connection = "Engine connection"
        mock_create_engine.return_value = expected_test_connection

        test_connection = get_db_connection(**_SETTINGS)

        mock_create_engine.assert_called_once_with(url)

        assert test_connection == mock_create_engine.return_value
