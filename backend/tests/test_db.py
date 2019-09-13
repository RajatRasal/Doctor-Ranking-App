"""
Tests for functions which connect to database and create, retrieve, update and
delete from the database.
"""
import mock
import pytest
from sqlalchemy import MetaData, Column, Integer, Table, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from src.model.tables import create_table_if_not_exists, drop_table_if_exists

class TestPostgresCRUD:

    @pytest.fixture(autouse=True)
    def setup_savepoint(self, request, test_db_conn):
        """ 
        Drops all tables in test db instance.
        """
        print('SETUP')
        self.engine = test_db_conn
        self.conn = test_db_conn.connect()
        self.metadata = MetaData(self.conn)
        self.trans = self.conn.begin()
        print('YIELD TO:', request.function.__name__)
        yield 
        self.trans.rollback()
        print('TEARDOWN')

    def test_create_new_table_and_returns_table_obj(self):
        """
        Inserts new table into db.
        """
        tablename = 'test_table'

        table = create_table_if_not_exists(tablename, self.conn, 
            Column('id', Integer))

        inspector = inspect(self.conn)
        new_table_names = inspector.get_table_names()

        assert tablename in new_table_names
        assert isinstance(table, Table)
        assert [str(col) for col in table.columns] == ['test_table.id']

    def test_table_not_created_if_name_already_exists_and_returns_none(self):
        """
        Inserts new table into db, adds data to that table, then tries to create
        the same table again. The second table should not be created.
        """
        tablename = 'test_table'
        test_table = create_table_if_not_exists(tablename, self.conn, 
            Column('test_id', Integer))

        insert_one = test_table.insert().values(test_id=1)
        self.conn.execute(insert_one)

        select_all = select([test_table])
        res = self.conn.execute(select_all).fetchall()
        assert len(res) == 1

        table = create_table_if_not_exists(tablename, self.conn,
            Column('test_id', Integer))

        res = self.conn.execute(select_all).fetchall()
        assert len(res) == 1
        assert table == None

    def test_no_col_given_for_create_new_table_return_false(self):
        """
        No action is performed if we attempt to create a table with no columns. 
        """
        assert False 


    def NOT_test_drop_table_if_exists_and_return_true(self):
        """
        Drops table from db if it exists.
        """
        assert True

    def NOT_test_table_not_deleted_if_not_exists_and_return_false(self):
        """
        No action is performed if we attempt to drop a non-existent table. 
        """
        assert True
