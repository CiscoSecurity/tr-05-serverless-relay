from flask import Blueprint

from api.utils import json_ok

respond_api = Blueprint('respond', __name__)


@respond_api.route('/respond/observables', methods=['POST'])
def respond_observables():
    # There are no actions to list.
    return json_ok([])


@respond_api.route('/respond/trigger', methods=['POST'])
def respond_trigger():
    # There are no actions to trigger.
    return json_ok({'status': 'failure'})
