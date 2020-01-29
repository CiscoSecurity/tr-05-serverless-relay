from flask import Blueprint

from api.utils import json_ok

health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    return json_ok({'status': 'ok'})
