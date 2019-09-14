"""
ORM functions for creating and deleting table definitions in the database,
equivalent to DDL only using SQLAlchemy's ORM instead of SQL.
"""
import sqlalchemy
from sqlalchemy import MetaData, Table, Integer, String, Column, ForeignKey, \
    CheckConstraint, inspect

from db_connection import get_db_connection

class PostgresDatabase:  # (DatabaseMixin):

    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.tablenames = []
        
    def create_table_if_not_exists(self, name, *cols):
        """
        Create a new table using the inputted connection engine and columns, given
        that a table of the same name does not already exist.
        """
        # Exit if inputs are empty
        if not (cols and self.db_conn):
            return None
    
        # Reflect db connetion to get existing schema from database
        meta = MetaData(self.db_conn)
        meta.reflect()

        # Create tables if they do not exist
        try:
            table = Table(name, meta, *cols)
            table.create(self.db_conn, checkfirst=True)
            self.tablenames.append(name)
            return table
        except sqlalchemy.exc.InvalidRequestError:
            return None

    def insert_unique_records_to_table(self, tablename, records):
        """
        """
        # Exit if inputs are empty
        if not (tablename and records):
            return None

        # 

        return None

def insert_unique_records_to_table(table, db_conn, records):
    if not (table and db_conn and records):
        return False
    return True

if __name__ == "__main__":
    import os
    import pandas as pd

    """
    engine = get_db_connection()

    # Drop all tables if they exist
    meta = MetaData(engine)
    meta.reflect()

    for tbl in reversed(meta.sorted_tables):
        engine.execute(tbl.delete())

    meta.drop_all()

    inspector = inspect(engine.connect())
    print(f'Start tables: {inspector.get_table_names()}')

    # Create diseases table
    diseases = create_table_if_not_exists('diseases', engine,
        Column('id', Integer, primary_key=True),
        Column('type', String, nullable=False))

    # Create Parameters table
    parameters = create_table_if_not_exists('parameters', engine,
        Column('id', Integer, primary_key=True),
        Column('type', String, nullable=False))

    # Create Disease-Parameters relationship table
    dis_param_link_name = 'disease_params_importance'
    disease_params_importance = create_table_if_not_exists(dis_param_link_name, engine,
        Column('disease_id', Integer, ForeignKey('diseases.id'), nullable=False, primary_key=True),
        Column('parameter_id', Integer, ForeignKey('parameters.id'), nullable=False, primary_key=True),
        Column('importance', Integer, CheckConstraint('importance >= 0 and importance <= 5'), nullable=False))

    inspector = inspect(engine.connect())
    print(f'New tables: {inspector.get_table_names()}')
    """

    backend_src_dir = os.path.dirname(os.path.abspath(__file__))
    data = f'{backend_src_dir}/../../tests/parameter_weight_test_data.csv'
    params_weights_df = pd.read_csv(data, skiprows=[0],
                                    index_col='Disease Name',
                                    usecols=range(17))
    params_weights_df.dropna(inplace=True)
    print(params_weights_df.to_dict('record'))
    # print(params_weights_df.head())
