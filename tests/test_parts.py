# this file is for creating test cases related to parts

# imports
from app.models import db, Part
from app import create_app
import unittest
# from datetime import datetime

# part test cases
class TestPart(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.part = Part(part_name="test_part", price=100.00)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.part)
            db.session.commit()
        self.client = self.app.test_client()

    # create part tests
    def test_create_part(self):
        part_payload = {
            "part_name": "tire",
            "price": 100.00
        }

        response = self.client.post('/inventory/', json=part_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['part_name'], "tire")

    def test_invalid_creation(self):
        part_payload = {
            "part_name": "tire"     
        }

        response = self.client.post('/inventory/', json=part_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['price'], ['Missing data for required field.'])

    # get parts test
    def test_get_parts(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)

    # update part tests
    def test_update_part(self):
        update_payload = {
            "part_name": "tire",
            "price": 150.00
        }

        response = self.client.put('/inventory/1', json=update_payload,)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['part_name'], 'tire') 
        self.assertEqual(response.json['price'], 150.00)

    def test_invalid_update(self):
        part_payload = {
            "part_name": "tire"      
        }

        response = self.client.put('/inventory/1', json=part_payload)
        self.assertIn(response.status_code, [400, 404])
        self.assertEqual(response.json['price'], ['Missing data for required field.'])

    # delete part tests
    def test_delete_part(self):
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('succesfully deleted part 1', response.get_data(as_text=True))

    def test_invalid_delete(self):
        response = self.client.delete('/inventory/999')
        self.assertEqual(response.status_code, 404)
