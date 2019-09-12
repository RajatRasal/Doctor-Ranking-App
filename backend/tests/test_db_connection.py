"""
Tests for establishing connections to database servers.
"""
import os

import mock
import pytest

class TestDatabaseConnection:

    def setup_method(self):
        """
        Setup postgres connection environment variables.
        """
        print('SETUP METHOD ###################')
        self.db = 'test_db'
        self.port = '1234' 
        self.user = 'test_user' 
        self.pwd = 'test_password' 
        self.host = 'test_host' 

        os.environ['PGDATABASE'] = self.db 
        os.environ['PGPORT'] = self.port 
        os.environ['PGUSER'] = self.user 
        os.environ['PGPASSWORD'] = self.pwd 
        os.environ['PGHOST'] = self.host 

    @mock.patch('src.model.db_connection._create_engine_wrapper')
    def test_default_connection_to_postgres(self, mock_create_engine):
        """
        Tests that URL for connection to postgres db is formed correctly and
        passed into sqlalchemy Engine object.
        """
        from src.model.db_connection import get_db_connection

        # Mock out return value of _create_engine_wrapper
        expected_test_connection = "Engine connection"
        mock_create_engine.return_value = expected_test_connection

        test_connection = get_db_connection()

        # Test call to wrapper
        url = f'postgres://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.db}'
        mock_create_engine.assert_called_once_with(url)

        # Test that the postgres connection engine is being returned directly
        # without any further changes to it.
        assert test_connection == mock_create_engine.return_value
