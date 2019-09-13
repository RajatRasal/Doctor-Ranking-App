"""
ORM functions for creating and deleting table definitions in the database,
equivalent to DDL only using SQLAlchemy's ORM instead of SQL.
"""
import sqlalchemy
from sqlalchemy import MetaData, Table, Integer, String, Column, ForeignKey, \
    inspect

from db_connection import get_db_connection

def create_table_if_not_exists(name, db_conn, *cols):
    """
    Create a new table using the inputted connection engine and columns, given
    that a table of the same name does not already exist.
    """
    # Exit if no columns given
    if not cols:
        return None

    # Reflect db connetion to get existing schema from database
    meta = MetaData(db_conn)
    meta.reflect()

    try:
        table = Table(name, meta, *cols)
        table.create(db_conn, checkfirst=True)
        return table
    except sqlalchemy.exc.InvalidRequestError:
        return None

# def drop_table_if_exists(name, db_conn):
#     pass

# def add_unique_records_to_table(table, records):
#     pass

if __name__ == "__main__":
    engine = get_db_connection()

    # Create diseases table
    diseases = create_table_if_not_exists('diseases', engine,
        Column('id', Integer, primary_key=True),
        Column('type', String))

    # Create Parameters table
    parameters = create_table_if_not_exists('parameters', engine,
        Column('id', Integer, primary_key=True),
        Column('type', String))

    # Create Disase-Parameters link table
    dis_param_link_name = 'disease_params_importance'
    disease_params_importance = create_table_if_not_exists(dis_param_link_name,
        engine,
        Column('disease_id', Integer, ForeignKey('diseases.id'), nullable=False),
        Column('parameter_id', Integer, ForeignKey('parameters.id'), nullable=False),
        Column('importance', Integer, nullable=False))

    inspector = inspect(engine.connect())
    print(f'Existing tables: {inspector.get_table_names()}')
