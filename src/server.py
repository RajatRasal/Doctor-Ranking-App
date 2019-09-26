import os

from flask import Flask, Blueprint, jsonify, current_app, render_template, \
    make_response, abort

try:
    from src.model.tables import PostgresDatabase
    from src.model.db_connection import get_db_connection
    from src.ranking_engine import HcpRankingEngine
except Exception:
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
def get_diseases():
    ranking_engine = current_app.config['hcp_rank_engine']
    all_diseases = ranking_engine.list_diseases()
    return jsonify({'diseases': all_diseases})

@hcp_engine.route('/diseases/<disease>', methods=['POST'])
def get_and_post_parameter_importance(disease):
    print(disease)
    ranking_engine = current_app.config['hcp_rank_engine']
    param_importance = ranking_engine.list_parameters(disease)
    res_json = [{'parameter': p, 'importance': i} for p, i in param_importance]
    print(res_json)
    return jsonify(res_json)

@hcp_engine.route('/diseases/<disease>', methods=['PUT'])
def update_parameter_importance(disease):
    pass

@hcp_engine.route('/doctors/count', methods=['GET'])
def get_doctors_count():
    ranking_engine = current_app.config['hcp_rank_engine']
    count = ranking_engine.count_doctors()
    return jsonify({'count': count})

@hcp_engine.route('/doctors/rank/<disease>/<int:top_limit>/<int:bottom_limit>', methods=['GET'])
def get_doctors_rank(disease, top_limit, bottom_limit):
    if top_limit <= 0 and bottom_limit <= 0:
        abort(400, 'Top needs a limit > 0')

    ranking_engine = current_app.config['hcp_rank_engine']
    doctors = ranking_engine.rank_doctors(disease)
    top = doctors[0:top_limit]
    bottom = doctors[-bottom_limit:]

    hcp_json_map = lambda pair: {'hcp_name': pair[0], 'score': pair[1]}
    res = {'top': list(map(hcp_json_map, top)),
           'bottom': list(map(hcp_json_map, bottom))}

    return jsonify(res)


if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run('0.0.0.0')
