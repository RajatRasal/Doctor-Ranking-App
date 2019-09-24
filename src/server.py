import os

from flask import Flask, Blueprint, jsonify, current_app, render_template, \
    make_response

from model.tables import PostgresDatabase
from model.db_connection import get_db_connection
from ranking_engine import HcpRankingEngine


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

hcp_engine.add_url_rule('/test', 'test', lambda: f'Hello World!')

dirname = os.path.dirname(os.path.abspath(__file__))
index_file = os.path.join(dirname, 'template/index.html')
# hcp_engine.add_url_rule('/', 'index', render_template('index.html'))

@hcp_engine.route('/', methods=['GET'])
def index():
    response = make_response(render_template('index.html'))
    response.headers.set('Cache-Control', 'no-store, must-revalidate')
    response.headers.set('Pragma', 'no-cache')
    response.headers.set('Expires', 0)
    return response


@hcp_engine.route('/diseases', methods=['GET'])
def diseases():
    ranking_engine = current_app.config['hcp_rank_engine']
    all_diseases = ranking_engine.list_diseases()
    return jsonify({'diseases': all_diseases})

if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run('0.0.0.0')
