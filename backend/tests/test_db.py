"""
Tests for functions which connect to database and create, retrieve, update and
delete from the database.
"""
import mock
import pytest
from sqlalchemy import MetaData, Column, Integer, inspect
from sqlalchemy.orm import sessionmaker

from src.model.tables import create_table_if_not_exists, drop_table_if_exists

class TestPostgresCRUD:

    @pytest.fixture(autouse=True)
    def setup_savepoint(self, request, test_db_conn):
        """ 
        Drops all tables in test db instance.
        """
        print('SETUP')
        self.conn = test_db_conn.connect()
        self.metadata = MetaData(self.conn)
        self.trans = self.conn.begin()
        print('YIELD TO:', request.function.__name__)
        yield 
        self.trans.rollback()
        print('TEARDOWN')

    def test_create_new_table(self):
        """
        Inserts new table into db.
        """
        tablename = 'diseases'

        create_table_if_not_exists(tablename, self.conn, Column('id', Integer))

        inspector = inspect(self.conn)
        new_table_names = inspector.get_table_names()

        assert len(new_table_names) == 1
        assert new_table_names[0] == tablename

    def test_no_col_given_for_create_new_table_return_false(self, test_db_conn):
        """
        Inserts new table into db.
        """
        # metadata = MetaData(test_db_conn)
        # res = create_table_if_not_exists('diseases', test_db_conn, []) 
        assert False


    def test_table_not_created_if_name_already_exists_and_returns_false(self):
        """
        No new table inserted if there is already a table with the same name in
        the database.
        """
        assert False

    def test_drop_table_if_exists_and_return_true(self):
        """
        Drops table from db if it exists.
        """
        assert False

    def test_table_not_deleted_if_not_exists_and_return_false(self):
        """
        No action is performed if we attempt to drop a non-existent table. 
        """
        assert False
