#services/pedidos/project/__init__.py


import os  #nuevo
from datetime import datetime
#from dateutil import parser as datetime_parser
#from dateutil.tz import tzutc
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy  # nuevo

# instanciamos la app
app = Flask(__name__)


# establelciendo configuracion
app_settings = os.getenv('APP_SETTINGS')   # Nuevo
app.config.from_object(app_settings)       # Nuevo

# instanciando la db
db = SQLAlchemy(app)  # nuevo


#modelo
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    items = db.relationship('Item', backref='product', lazy='dynamic')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),
                            index=True)
    date = db.Column(db.DateTime, default=datetime.now)
    items = db.relationship('Item', backref='order', lazy='dynamic',
                            cascade='all, delete-orphan')


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),
                           index=True)
    quantity = db.Column(db.Integer)
    
        
#rutas
@app.route('/pedidos/ping', methods=['GET'])
def ping_pong():
   return jsonify({
       'status':'success',
       'message': 'pong'
   })

