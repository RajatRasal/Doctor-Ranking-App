"""
ORM functions for creating and deleting table definitions in the database,
equivalent to DDL only using SQLAlchemy's ORM instead of SQL.
"""
import sqlalchemy
from sqlalchemy import MetaData, Table, Integer, String, Column, ForeignKey, \
    CheckConstraint, inspect
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoSuchTableError, IntegrityError

from db_connection import get_db_connection

class PostgresDatabase:  # (DatabaseMixin):

    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.meta = MetaData(self.db_conn)
        self.session = Session(self.db_conn)
        
    def create_table_if_not_exists(self, name, *cols):
        """
        Create a new table using the inputted connection engine and columns,
        given that a table of the same name does not already exist.
        """
        if not (cols and self.db_conn):
            return None
    
        # Reflect db connetion to get existing schema from database
        # self.meta = MetaData(self.db_conn)
        self.meta.reflect()

        try:
            table = Table(name, self.meta, *cols)
            table.create(self.db_conn, checkfirst=True)
            # self.tablenames.append(name)
            return table
        except sqlalchemy.exc.InvalidRequestError:
            return None

    def get_or_create_records_in_table(self, tablename, records):
        self.meta.reflect()

        try:
            table = self.meta.tables[tablename]
        except KeyError:
            raise NoSuchTableError(tablename)

        res_list = []

        try:
            for record in records:
                res = self.session.query(table).filter_by(**record).first()
                if not res:
                    self.db_conn.execute(table.insert().values(record))
                    res = self.session.query(table).filter_by(**record).first()
                    res_list.append((res, True))
                else:
                    res_list.append((res, False))
        except IntegrityError as e:
            self.rollback()
            raise e

        return res_list

    def find_record_in_table(self, tablename, **kwargs):
        pass

    def rollback(self):
        self.session.rollback()
        self.session = Session(self.db_conn)

    def commit(self):
        self.session.commit()


if __name__ == "__main__":
    import os
    import pandas as pd
    import numpy as np

    engine = get_db_connection()
    connection = engine.connect()

    db = PostgresDatabase(connection)
    """

    # Drop all tables if they exist
    meta = MetaData(engine)
    meta.reflect()

    for tbl in reversed(meta.sorted_tables):
        engine.execute(tbl.delete())

    meta.drop_all()

    inspector = inspect(engine.connect())
    print(f'Start tables: {inspector.get_table_names()}')

    # Create diseases table
    diseases = db.create_table_if_not_exists('diseases', engine,
        Column('id', Integer, primary_key=True),
        Column('type', String, nullable=False))

    # Create Parameters table
    parameters = db.create_table_if_not_exists('parameters', engine,
        Column('id', Integer, primary_key=True),
        Column('type', String, nullable=False))

    # Create Disease-Parameters relationship table
    dis_param_link_name = 'disease_params_importance'
    disease_params_importance = db.create_table_if_not_exists(dis_param_link_name, engine,
        Column('disease_id', Integer, ForeignKey('diseases.id'), nullable=False, primary_key=True),
        Column('parameter_id', Integer, ForeignKey('parameters.id'), nullable=False, primary_key=True),
        Column('importance', Integer, CheckConstraint('importance >= 0 and importance <= 5'), nullable=False))

    inspector = inspect(engine.connect())
    print(f'New tables: {inspector.get_table_names()}')
    """

    # Load Disease types and their associated parameters.
    backend_src_dir = os.path.dirname(os.path.abspath(__file__))
    data = f'{backend_src_dir}/../../tests/parameter_weight_test_data.csv'
    params_weights_df = pd.read_csv(data, skiprows=[0],
                                    index_col='Disease Name',
                                    usecols=range(17))
    params_weights_df.dropna(inplace=True)

    # Inserting all new disease types into database table.
    diseases = list(params_weights_df.index)
    disease_records = map(lambda x: {'type': x}, diseases)
    res = db.insert_unique_records_to_table('diseases', disease_records)
    db.commit()

    # Inserting all new parameter types into parameter table.
    cols = ['P' + str(i) for i in range(1, 9)]
    all_params = params_weights_df[cols].values.flatten()
    params = list(np.unique(all_params))
    params_records = map(lambda x: {'type': x}, params)
    res = db.insert_unique_records_to_table('parameters', params_records)
    db.commit()

    # Get id names
