from flask import Blueprint

from api.schemas import DashboardPeriodSchema
from api.utils import jsonify_data, get_jwt, get_params


dashboard_api = Blueprint('dashboard', __name__)


@dashboard_api.route('/dashboard/tiles', methods=['GET'])
def tiles():
    _ = get_jwt()
    return jsonify_data([])


@dashboard_api.route('/dashboard/tiles/<module_instants_id>/<tile_id>',
                     methods=['GET'])
def tile(module_instants_id, tile_id):
    _ = get_jwt()
    return jsonify_data({})


@dashboard_api.route('/dashboard/tiles/<module_instants_id>/<tile_id>/data',
                     methods=['GET'])
def tile_data(module_instants_id, tile_id):
    _ = get_jwt()
    _ = get_params(DashboardPeriodSchema())
    return jsonify_data({})
