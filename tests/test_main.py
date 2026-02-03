import unittest
from unittest.mock import patch
from main import swapi_proxy
from flask import Flask

class TestSwapiProxy(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    @patch('requests.get')
    def test_sucesso_luke_skywalker(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "Luke Skywalker"}

        with self.app.test_request_context('/consultar?categoria=people&id=1&key=TEST'):
            from flask import request
            response, status = swapi_proxy(request)
            
            data = response.get_json()
            self.assertEqual(status, 200)
            self.assertEqual(data['payload']['name'], "Luke Skywalker")
            self.assertIn('ui_navigation', data) 

    def test_falha_sem_categoria(self):
        with self.app.test_request_context('/consultar?key=TEST'):
            from flask import request
            self.assertIsNotNone(swapi_proxy(request))

if __name__ == '__main__':
    unittest.main()