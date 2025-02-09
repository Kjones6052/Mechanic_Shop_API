# this file is for creating test cases related to mechanics

# imports
from app.models import db, Mechanic
from app import create_app
import unittest
# from datetime import datetime

# mechanic test cases
class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(name="test_mechanic", email="test@email.com", phone="4445557777", salary=100.00)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()

    # create mechanic tests
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Joe Mechanic",
            "email": "icanfixit@email.com",
            "phone": "9998887777",
            "salary": 100.00
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Joe Mechanic")

    def test_invalid_creation(self):
        mechanic_payload = {
            "name": "Moe Mechanic",
            "phone": "9998887777",
            "salary": 125.00       
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    # get all mechanics test
    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)

    # update mechanic tests
    def test_update_mechanic(self):
        update_payload = {
            "name": "Peter",
            "phone": "5558889999",
            "email": "example@email.com",
            "salary": 150.00
        }

        response = self.client.put('/mechanics/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter') 
        self.assertEqual(response.json['email'], 'example@email.com')

    def test_invalid_update(self):
        mechanic_payload = {
            "name": "Joe Mechanic",
            "email": "test@email.com",
            "salary": 135.00       
        }

        response = self.client.put('/mechanics/1', json=mechanic_payload)
        self.assertEqual(response.status_code, [400, 404])
        self.assertIn(response.json['phone'], ['Missing data for required field.'])
        self.assertIn('customer not found', response.get_data(as_text=True))
        self.assertIn('Missing data for required field.', response.get_data(as_text=True))

    # delete mechanic tests
    def test_delete_mechanic(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('succesfully deleted mechanic 1', response.get_data(as_text=True))

    def test_invalid_delete(self):
        response = self.client.delete('/mechanics/999')
        self.assertEqual(response.status_code, 404)

    # most valuable mechanic tests
    def test_most_valuable_mechanic(self):
        response = self.client.get('/mechanics/mvm')
        self.assertEqual(response.status_code, 200)
