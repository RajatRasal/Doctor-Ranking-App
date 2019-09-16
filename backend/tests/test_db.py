"""
Tests for functions which connect to database and create, retrieve, update and
delete from the database.
"""
import mock
import pandas as pd
import pytest
from sqlalchemy import MetaData, Column, Integer, String, Table, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.exc import NoSuchTableError, IntegrityError

from tests.helper import does_not_raise
from src.model.tables import PostgresDatabase

class TestPostgresCreate:

    @pytest.fixture(autouse=True)
    def setup_savepoint(self, request, test_db_conn):
        """ 
        Drops all tables in test db instance.
        """
        print('SETUP')
        self.engine = test_db_conn
        self.conn = self.engine.connect()
        self.trans = self.conn.begin()
        self.database = PostgresDatabase(self.conn)
        self.metadata = MetaData(self.database.db_conn)
        print('YIELD TO:', request.function.__name__)
        yield 
        self.trans.rollback()
        print('TEARDOWN')

    def test_create_new_table_and_returns_table_obj(self):
        """
        Inserts new table into db.
        """
        tablename = 'test_table'

        table = self.database.create_table_if_not_exists(tablename,
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
        test_table = self.database.create_table_if_not_exists(tablename,
            Column('test_id', Integer))

        insert_one = test_table.insert().values(test_id=1)
        self.conn.execute(insert_one)

        select_all = select([test_table])
        res = self.conn.execute(select_all).fetchall()

        assert len(res) == 1

        table = self.database.create_table_if_not_exists(tablename,
            Column('test_id', Integer))

        res = self.conn.execute(select_all).fetchall()

        assert len(res) == 1
        assert table == None

    def test_no_col_given_for_create_new_table_return_false(self):
        """
        No action is performed if we attempt to create a table with no columns. 
        There should be no changes to the database schema.
        """
        table = self.database.create_table_if_not_exists('test_table')

        inspector = inspect(self.conn)
        table_names = inspector.get_table_names()

        assert table == None
        assert 'test_table' not in table_names

class TestPostgresGetOrInsertRecords:

    @pytest.fixture(autouse=True)
    def setup_savepoint(self, request, test_db_conn):
        """ 
        Drops all tables in test db instance.
        """
        print('SETUP')
        self.engine = test_db_conn
        self.conn = self.engine.connect()
        self.trans = self.conn.begin()
        self.metadata = MetaData(self.conn)
        tablename = 'test_table'
        table = Table(tablename, self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String))
        table.create(self.conn)
        self.database = PostgresDatabase(self.conn)
        # self.database.create_table_if_not_exists('test_table',
        #     Column('id', Integer, primary_key=True), Column('name', String))
        print('YIELD TO:', request.function.__name__)
        yield 
        self.trans.rollback()
        print('TEARDOWN')

    @pytest.mark.parametrize('tablename, df, expectation', [
        ('test_table', [], does_not_raise()),
        ('', [{'x': 'x'}], pytest.raises(NoSuchTableError)),
    ])
    def test_insert_into_erroneous_input_behaviour(self, tablename, df,
                                                   expectation):
        """
        No action is performed when no records are input to be inserted into the
        table and False is returned.
        """
        with expectation:
            self.database.get_or_create_records_in_table(tablename, df)

    def test_insert_into_table_empty_record_returns_nothing(self):
        tablename = 'test_table'
        res = self.database.get_or_create_records_in_table(tablename, [])
        assert res == []

    def test_insert_into_table_new_records(self):
        records = [(1, 'name1'), (2, 'name2')]
        tablename = 'test_table'
        df = pd.DataFrame(records, columns=['id', 'name']) 
        data = df.to_dict('records')

        res = self.database.get_or_create_records_in_table(tablename, data)
        expected = list(map(lambda rec: (rec, True), records))

        self.metadata.reflect()

        table = self.database.meta.tables[tablename]
        select_all = list(self.database.db_conn.execute(select([table])))

        assert select_all == records
        assert res == expected

    def test_insert_into_table_if_not_exists_fails(self):
        records = [(1, 'name1'), (2, 'name2')]
        df = pd.DataFrame(records, columns=['id', 'name']) 
        data = df.to_dict('records')

        with pytest.raises(NoSuchTableError):
            self.database.get_or_create_records_in_table('x', data)

    def test_insert_into_table_fails_if_entering_same_row_twice(self):
        """
        """
        records = [(1, 'name1'), (2, 'name2')]
        tablename = 'test_table'
        df = pd.DataFrame(records, columns=['id', 'name']) 
        data = df.to_dict('records')

        res1 = self.database.get_or_create_records_in_table(tablename, data)
        res2 = self.database.get_or_create_records_in_table(tablename, data)

        assert res1 == list(map(lambda x: (x, True), records))
        assert res2 == list(map(lambda x: (x, False), records))

        self.metadata.reflect()
        table = self.database.meta.tables[tablename]
        select_all = list(self.database.db_conn.execute(select([table])))
        print(select_all)

        assert select_all == records

    def test_insert_into_table_fails_if_entering_duplicates(self):
        records = [(1, 'name1'), (1, 'name1')]
        tablename = 'test_table'
        df = pd.DataFrame(records, columns=['id', 'name']) 
        data = df.to_dict('records')

        res = self.database.get_or_create_records_in_table(tablename, data)

        assert res == [((1, 'name1'), True), ((1, 'name1'), False)]

        self.metadata.reflect()
        table = self.database.meta.tables[tablename]
        select_all = list(self.database.db_conn.execute(select([table])))

        assert select_all == [(1, 'name1')]

    @mock.patch('src.model.tables.PostgresDatabase.rollback')
    def test_insert_into_table_fails_if_entering_duplicate_pkeys(self, patch):
        records = [(1, 'name1'), (1, 'name2')]
        tablename = 'test_table'
        df = pd.DataFrame(records, columns=['id', 'name']) 
        data = df.to_dict('records')

        with pytest.raises(IntegrityError):
            self.database.get_or_create_records_in_table(tablename, data)
            patch.assert_called_once()

    def test_get_record_from_table_without_insert(self):
        # Insert records in fixture
        # Get them using get_or_create
        # Check that correct record is got and existing records are the same
        assert False

    def test_get_record_from_table_based_on_partial_input_without_insert(self):
        assert False

    def test_get_multiple_records_from_table_without_insert(self):
        assert False

    def test_get_multiple_partial_records_from_table_without_insert(self):
        assert False
