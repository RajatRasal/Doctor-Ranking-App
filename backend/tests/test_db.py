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

from src.model.tables import PostgresDatabase  # insert_unique_records_to_table
# create_table_if_not_exists, \

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

class TestPostgresInsert:

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
        self.database.create_table_if_not_exists('test_table',
            Column('id', Integer), Column('name', String))
        self.metadata = MetaData(self.database.db_conn)
        print('YIELD TO:', request.function.__name__)
        yield 
        self.trans.rollback()
        print('TEARDOWN')

    @pytest.mark.parametrize('tablename,df,expected', [
        ('test_table', [], False),
        ('', [{'x': 'x'}], False),
        ('test_table', [{'x': 'x'}], True)
    ])
    def test_insert_record_input_validation(self, tablename, df, expected):
        """
        No action is performed when no records are input to be inserted into the
        table and False is returned.
        """
        res = self.database._PostgresDatabase__insert_validation(tablename, df)
        assert res == expected

    @mock.patch('src.model.tables.PostgresDatabase._PostgresDatabase__insert_validation')
    @mock.patch('src.model.tables.PostgresDatabase._PostgresDatabase__insert_helper')
    @pytest.mark.parametrize('valid, helper, expected', [
        (True, True, True),
        (False, True, False),
        (True, False, False),
        (False, False, False)
    ])
    def test_no_action_when_no_tablename_is_given_for_inserting(self,
                                                                patch_helper,
                                                                patch_validation,
                                                                valid,
                                                                helper,
                                                                expected):
        """
        Behaviour of insert into table function.
        """
        patch_helper.return_value = valid
        patch_validation.return_value = helper
        res = self.database.insert_unique_records_to_table('test_tbl',
                                                           pd.DataFrame())

        assert patch_validation.call_count == 1
        assert patch_helper.call_count == int(valid)

        assert res == expected

    def test_insert_into_table_new_records(self):
        records = [(1, 'name1'), (2, 'name2')]
        tablename = 'test_table'
        df = pd.DataFrame(records, columns=['id', 'name']) 
        data = df.to_dict('records')

        res = self.database._PostgresDatabase__insert_helper(tablename, data)

        self.metadata.reflect()

        table = self.database.meta.tables[tablename]
        select_all = list(self.database.db_conn.execute(select([table])))

        assert select_all == records
        assert res == True

    def test_insert_into_table_if_not_exists_fails(self):
        records = [(1, 'name1'), (2, 'name2')]
        df = pd.DataFrame(records, columns=['id', 'name']) 
        data = df.to_dict('records')

        res = self.database._PostgresDatabase__insert_helper('x', data)

        return res == False

    def test_insert_into_table_fails_if_entering_same_row_twice(self):
        """
        """
        records = [(1, 'name1'), (2, 'name2')]
        tablename = 'test_table'
        df = pd.DataFrame(records, columns=['id', 'name']) 
        data = df.to_dict('records')

        res1 = self.database._PostgresDatabase__insert_helper(tablename, data)
        res2 = self.database._PostgresDatabase__insert_helper(tablename, data)

        assert res1
        assert res2

        self.metadata.reflect()
        table = self.database.meta.tables[tablename]
        select_all = list(self.database.db_conn.execute(select([table])))
        print(select_all)

        assert select_all == records

    def test_insert_into_table_fails_if_entering_duplicates(self):
        assert False
