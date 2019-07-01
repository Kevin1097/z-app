# services/pedidos/project/api/pedidos.py


from flask import Blueprint, jsonify, request, render_template

from project.api.models import Customer
from project import db
from sqlalchemy import exc


pedidos_blueprint = Blueprint('customers', __name__, template_folder='./templates')


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
            response_object['message'] = f'{name} ha sido agregado!'
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
    response_object = {
        'status': 'failed',
        'message': 'El customer no existe'
    }
    try:
      customer = Customer.query.filter_by(id=int(customer_id)).first()
      if not customer:
          return jsonify(response_object), 404
      else:
        response_object = {
          'status':'success',
          'data':{
            'id':customer.id,
            'name':customer.name
          }
        }
        return jsonify(response_object), 200
    except ValueError:
      return jsonify(response_object), 404

@pedidos_blueprint.route('/customers', methods=['GET'])
def get_all_customers():
    """Obteniendo todos los customers"""
    response_object = {
        'status': 'success',
        'data': {
            'customer': [customer.to_json() for customer in Customer.query.all()]
        }
    }
    return jsonify(response_object), 200

@pedidos_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(Customer(name=name))
        db.session.commit()
    customer = Customer.query.all()
    return render_template('index.html', customers=customer)