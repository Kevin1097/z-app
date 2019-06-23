# services/pedidos/project/api/pedidos.py


from flask import Blueprint, jsonify


pedidos_blueprint = Blueprint('pedidos', __name__)


@pedidos_blueprint.route('/pedidos/ping', methods=['GET'])
def ping_pong():
  return jsonify({
    'status': 'success',
    'message': 'pong'
  })