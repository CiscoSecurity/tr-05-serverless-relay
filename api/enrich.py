from flask import Blueprint

from api.utils import json_ok

enrich_api = Blueprint('enrich', __name__)


@enrich_api.route('/deliberate/observables', methods=['POST'])
def deliberate_observables():
    # TODO: extract observables from request
    return json_ok({})


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    # TODO: extract observables from request
    return json_ok({})


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    # TODO: extract observables from request
    return json_ok([])
