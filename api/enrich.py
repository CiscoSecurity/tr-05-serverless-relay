from flask import Blueprint

from api.utils import jsonify_data

enrich_api = Blueprint('enrich', __name__)


@enrich_api.route('/deliberate/observables', methods=['POST'])
def deliberate_observables():
    return jsonify_data({})


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    return jsonify_data({})


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    return jsonify_data([])
