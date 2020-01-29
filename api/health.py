from flask import Blueprint

from api.utils import jsonify_data

health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    return jsonify_data({'status': 'ok'})
