"""
Engine is responsible for handling requests from the user by querying in the
backend database or for getting the result of the ranking algorithm.
"""
import os

from sqlalchemy.orm import sessionmaker

try:
    from model.db_connection import get_db_connection
except:
    from src.model.db_connection import get_db_connection


class HcpRankingEngine:

    def __init__(self, db):
        self.db = db
        self.engine = get_db_connection()

    def list_diseases(self):
        res = self.db.findall_records_in_table('diseases', 'type')
        return [row[0] for row in res]

    def list_parameters(self, disease):
        session = sessionmaker(bind=self.engine)()
        res = []

        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            x = os.path.join(current_dir, 'model/list_all_params_for_disease.sql')
            with open(x, 'r') as f:
                x = ''.join(f.readlines()).replace('\n', ' ').format(disease=disease)
            res = [row for row in session.execute(x)]
        except:
            session.rollback()
        finally:
            session.close()
        return res

    def count_doctors(self):
        session = sessionmaker(bind=self.engine)()
        count = 0

        try:
            query = 'select count(distinct hcp_number) from doctors'
            count = session.execute(query).first()[0]
        except:
            session.rollback()
        finally:
            session.close()

        return count

    def rank_doctors(self, disease):
        pass

if __name__ == "__main__":
    from model.tables import PostgresDatabase
    from model.db_connection import get_db_connection

    engine = get_db_connection()
    db_conn = engine.connect()
    db = PostgresDatabase(db_conn)
    ranking_engine = HcpRankingEngine(db)

    print(ranking_engine.list_diseases())
