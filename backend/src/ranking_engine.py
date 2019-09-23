"""
Engine is responsible for handling requests from the user by querying in the
backend database or for getting the result of the ranking algorithm.
"""
class HcpRankingEngine:

    def __init__(self, db):
        self.db = db

    def list_diseases(self):
        res = self.db.findall_records_in_table('diseases', 'type')
        return [row[0] for row in res]


if __name__ == "__main__":
    from model.tables import PostgresDatabase
    from model.db_connection import get_db_connection

    engine = get_db_connection()
    db_conn = engine.connect()
    db = PostgresDatabase(db_conn)
    ranking_engine = HcpRankingEngine(db)

    print(ranking_engine.list_diseases())
