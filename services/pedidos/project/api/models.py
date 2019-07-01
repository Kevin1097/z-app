# services/pedidos/project/api/models.py


from datetime import datetime
from project import db


# modelo
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __init__(self, name):
        self.name = name


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), index=True)
    items = db.relationship('Item', backref='product', lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __init__(self, name):
        self.name = name


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),
                            index=True)
    date = db.Column(db.DateTime, default=datetime.now)
    items = db.relationship('Item', backref='order', lazy='dynamic',
                            cascade='all, delete-orphan')

    def to_json(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'date': self.date
        }

    def __init__(self, customer_id, date):
        self.customer_id = customer_id
        self.date = date


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),
                           index=True)
    quantity = db.Column(db.Integer)

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }

    def __init__(self, order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
