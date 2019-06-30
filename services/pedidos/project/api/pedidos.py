# services/pedidos/project/api/pedidos.py


from flask import Blueprint, jsonify, request

from project.api.models import Customer
from project import db
from sqlalchemy import exc


pedidos_blueprint = Blueprint('pedidos', __name__)


@pedidos_blueprint.route('/pedidos/ping', methods=['GET'])
def ping_pong():
  return jsonify({
    'status': 'success',
    'message': 'pong'
  })

@pedidos_blueprint.route('/customers', methods=['POST'])
def add_customer():
    post_data = request.get_json()
    response_object = {
        'status': 'failed',
        'message': 'Carga invalida.'
    }
    if not post_data:
        return jsonify(response_object), 400
    name = post_data.get('name')
    try:
        customer = Customer.query.filter_by(name=name).first()
        if not customer:
            db.session.add(Customer(name=name))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{name} ha sido agregado !'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Lo siento. El usuario ya existe'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400

@pedidos_blueprint.route('/customers/<customer_id>', methods=['GET'])
def get_single_customer(customer_id):
    """Obtener detalles de usuario único"""
    customer = Customer.query.filter_by(id=customer_id).first()
    response_object = {
        'status': 'success',
        'data': {
            'id': customer.id,
            'name': customer.name
        }
    }
    return jsonify(response_object), 200