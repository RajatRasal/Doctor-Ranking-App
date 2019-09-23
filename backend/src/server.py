from flask import Flask, Blueprint, jsonify, current_app

from src.model.tables import PostgresDatabase
from src.model.db_connection import get_db_connection
from src.ranking_engine import HcpRankingEngine


hcp_engine = Blueprint('hcp_engine', __name__)

def create_app():
    global hcp_engine

    app = Flask(__name__)
    app.register_blueprint(hcp_engine)

    engine = get_db_connection()
    connection = engine.connect()
    database_interface = PostgresDatabase(connection)
    app.config['hcp_rank_engine'] = HcpRankingEngine(database_interface)

    return app

hcp_engine.add_url_rule('/', 'test', lambda: f'Hello World!')

@hcp_engine.route('/diseases', methods=['GET'])
def diseases():
    ranking_engine = current_app.config['hcp_rank_engine']
    all_diseases = ranking_engine.list_diseases()
    return jsonify({'diseases': all_diseases})

if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run('0.0.0.0')
