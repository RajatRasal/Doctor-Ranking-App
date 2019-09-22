"""
Test wiring of the Flask server controller functions which connect to the
backend model.
"""
import mock
import pytest

from tests.helper import does_not_raise
from src.server import create_app

class TestFlaskServer:

    def setup(self):
        print('SETUP')
        self.server = create_app().test_client()
        """
        self.engine = test_db_conn
        self.conn = self.engine.connect()
        self.trans = self.conn.begin()
        self.database = PostgresDatabase(self.conn)
        self.metadata = MetaData(self.database.db_conn)
        print('YIELD TO:', request.function.__name__)
        yield 
        self.trans.rollback()
        print('TEARDOWN')
        """

    def test_sanity_check(self):
        response = self.server.get('/')
        assert response.status_code == 200

    def DONOT_test_server_gets_list_of_diseases_and_returns_200(self):
        assert False

    def DONOT_test_server_gets_fails_to_get_diseases_list_and_returns_400(self):
        assert False
