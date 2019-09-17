"""
ORM functions for creating and deleting table definitions in the database,
equivalent to DDL only using SQLAlchemy's ORM instead of SQL.
"""
from itertools import product

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
                    self.session.execute(table.insert(), [record])
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

    """
    # Load Disease types and their associated parameters.
    backend_src_dir = os.path.dirname(os.path.abspath(__file__))
    data = f'{backend_src_dir}/../../tests/parameter_weight_test_data.csv'
    params_weights_df = pd.read_csv(data, skiprows=[0],
                                    index_col='Disease Name',
                                    usecols=range(17))
    params_weights_df.dropna(inplace=True)
    params_weights_df.index = params_weights_df.index.str.lower()

    cols = ['P' + str(i) for i in range(1, 9)]
    params_weights_df[cols] = params_weights_df[cols] \
        .apply(lambda col: col.str.lower())

    weight_cols = [col + ' Weight' for col in cols]
    weights_df = params_weights_df[weight_cols]
    params_weights_df[weight_cols] = weights_df \
        .where(weights_df >= 0, 0) \
        .where(weights_df <= 5, 5)

    # Inserting all new disease types into database table.
    diseases = list(disease for disease in params_weights_df.index)
    disease_records = map(lambda x: {'type': x}, diseases)
    disease_res = db.get_or_create_records_in_table('diseases', disease_records)
    db.commit()

    # Inserting all new parameter types into parameter table.
    all_params = params_weights_df[cols].values.flatten()
    params = list(param for param in np.unique(all_params))
    params_records = map(lambda x: {'type': x}, params)
    params_res = db.get_or_create_records_in_table('parameters', params_records)
    # print(params_res)
    params_res_map = {param:_id for (_id, param), _ in params_res}
    # print(params_res_map)
    db.commit()

    # Collecting disease_id and param_id pairs, together with weights and
    # inserting all of this into the disease_params_importance relationship table.

    # Below algorithm is currently Ω(n^2), but can be made better by loading the
    # disease_res and params_res lists into dictionaries.
    for (disease_id, disease), _ in disease_res:
        print(f'Inserting disease {disease} into link table')
        disease_params = params_weights_df.loc[disease, cols]
        param_ids = disease_params.map(params_res_map).to_list()
        weights = params_weights_df.loc[disease, weight_cols].to_list()

        link_records = []
        for param_id, weight in zip(param_ids, weights):
            link_records.append({'disease_id': disease_id,
                                 'parameter_id': param_id,
                                 'importance': weight})

        res = db.get_or_create_records_in_table('disease_params_importance',
                                                link_records)
    db.commit()
    """

    # Load Disease types and their associated parameters.
    backend_src_dir = os.path.dirname(os.path.abspath(__file__))
    data = f'{backend_src_dir}/../../tests/hcp_weightage_test_data.csv'
    hcp_weight_df = pd.read_csv(data, index_col='HCP Number')

    hcp_weight_df.index.name = 'hcp_number'
    # new_cols = ['hcp_number'] + [f'weight_{i}' for i in range(1, 6)]
    # new_col_names = dict(zip(hcp_weight_df.columns, new_cols)) 
    # hcp_weight_df.rename(columns=new_col_names, inplace=True)

    hcp_weight_df = hcp_weight_df \
       .where(hcp_weight_df >= 0, 0) \
       .where(hcp_weight_df <= 5, 5)

    hcp_weight_df.index = hcp_weight_df.index \
        .str \
        .slice(3) \
        .astype(int)

    # Create diseases table
    doctors = db.create_table_if_not_exists('doctors',
        Column('hcp_number', Integer, nullable=False),
        Column('weight_no', Integer, CheckConstraint('weight_no >= 0'), default=0),
        Column('weight', Integer, CheckConstraint('weight >= 0 and weight <= 5'), default=0))

    hcp_weight_records = hcp_weight_df.to_dict()
    for i, col in enumerate(hcp_weight_df.columns):
        dict_map = lambda _id, weight_no, weight: {'hcp_number': _id,
                                                   'weight_no': weight_no,
                                                   'weight': weight}
        records = [dict_map(_id, i, weight) 
                   for _id, weight in hcp_weight_records[col].items()]
        db.get_or_create_records_in_table('doctors', records)

    print(hcp_weight_records)

    # for col in hcp_weight_df.columns:
    #    print(hcp_weight_records[col])
    # res = db.get_or_create_records_in_table('doctors', hcp_weight_records) 

    db.commit()
