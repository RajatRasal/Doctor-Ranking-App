"""
Tests for functions which connect to database and create, retrieve, update and
delete from the database.
"""
import mock
import pytest
from sqlalchemy import MetaData, Column, Integer, Table, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from src.model.tables import create_table_if_not_exists, \
        insert_unique_records_to_table

class TestPostgresCRUD:

    @pytest.fixture(autouse=True)
    def setup_savepoint(self, request, test_db_conn):
        """ 
        Drops all tables in test db instance.
        """
        print('SETUP')
        self.engine = test_db_conn
        self.conn = test_db_conn.connect()
        self.session = sessionmaker(self.conn)()
        self.session.begin_nested()
        self.metadata = MetaData(self.conn)
        self.trans = self.conn.begin()
        print('YIELD TO:', request.function.__name__)
        yield 
        self.session.rollback()
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
        There should be no changes to the database schema.
        """
        table = create_table_if_not_exists('test_table', self.conn)

        inspector = inspect(self.conn)
        table_names = inspector.get_table_names()

        assert table == None
        assert 'test_table' not in table_names

    def test_no_records_given_for_inserting_returns_false(self):
        """
        No action is performed when no records are input to be inserted into the
        table and False is returned.
        """
        tablename = 'test_table'
        table = create_table_if_not_exists(tablename, self.conn,
            Column('test_id', Integer))

        res = insert_unique_records_to_table(tablename, self.conn, [])

        query_res = self.session.execute(table.select())

        assert not list(query_res)
        assert res == False 

    def test_no_action_when_no_tablename_is_given_for_inserting(self):
        """
        No action is performed when there is no tablename given for inserting
        unique records into.
        """
        res = insert_unique_records_to_table('', self.conn, [['x']])
        assert not res
