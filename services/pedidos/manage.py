# services/pedidos/manage.py


import unittest

from flask.cli import FlaskGroup

from project import create_app, db # nuevo
from project.api.models import Customer,Product,Order,Item

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Ejecutar las pruebas sin covertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('seed_db')
def seed_db():
    """Sembrado en la base de datos"""
    db.session.add(Customer(name='kevinmogollon'))
    db.session.add(Customer(name='abelhuanca'))
    db.session.commit()


if __name__ == '__main__':
   cli()
