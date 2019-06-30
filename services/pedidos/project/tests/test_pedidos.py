# services/pedidos/project/tests/test_pedidos.py


import json
import unittest
from project import db
from project.api.models import Customer
from project.tests.base import BaseTestCase


class TestPedidosService(BaseTestCase):
    """Tests for the Users Service."""

    def test_pedidos(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/pedidos/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_customer(self):
        """Agregando un nuevo cliente."""
        with self.client:
            response = self.client.post(
                '/customers',
                data=json.dumps({
                    'name': 'kevinmogollon'
                }),
                content_type = 'application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('kevinmogollon ha sido agregado !', data['message'])
            self.assertIn('success', data['status'])

    def test_add_customer_invalid_json(self):
        """Asegurando que se produzca un error si el objeto json esta vacío."""
        with self.client:
            response = self.client.post(
                '/customers',
                data=json.dumps({}),
                content_type = 'application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga invalida.', data['message'])
            self.assertIn('failed', data['status'])
    
    def test_add_customer_duplicate_name(self):
        """Asegurando que se produzca un error si el nombre ya existe."""
        with self.client:
            response = self.client.post(
                '/customers',
                data=json.dumps({
                    'name':'kevinmogollon'
                }),
                content_type = 'application/json',
            )
            response = self.client.post(
                '/customers',
                data=json.dumps({
                    'name':'kevinmogollon'
                }),
                content_type = 'application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Lo siento. El usuario ya existe', data['message'])
            self.assertIn('failed', data['status'])


if __name__ == '__main__':
    unittest.main()
