# this file is for creating test cases related to customers

# imports
from app.models import db, Customer
from app import create_app
import unittest
# from datetime import datetime
from app.utils.util import encode_token

# Customer test cases
class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="test_customer", email="test@email.com", phone="1112223333", password='test')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    # create customer tests
    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "2223334444",
            "password": "testpassword"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
        self.assertEqual(response.json['email'], "jd@email.com")
        self.assertEqual(response.json['phone'], "2223334444")
        self.assertEqual(response.json['password'], "testpassword")

    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"       
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing data for required field.', response.get_data(as_text=True))

    # customer login tests
    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'invalid email or password')

    # get all customers tests
    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    # get customer by id tests
    def test_get_customer_by_id(self):
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_customer_by_id(self):
        response = self.client.get('/customers/999')
        self.assertIn(response.status_code, [400, 404])
        self.assertIn('invalid customer id', response.get_data(as_text=True))
        self.assertIn('customer not found', response.get_data(as_text=True))
    
    # update customer tests
    def test_update_customer(self):
        update_payload = {
            "name": "Peter",
            "phone": "5558889999",
            "email": "test@email.com",
            "password": "testpw"
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}

        response = self.client.put('/customers/1', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Peter")
        self.assertEqual(response.json['email'], "test@email.com")
        self.assertEqual(response.json['phone'], "5558889999")
        self.assertEqual(response.json['password'], "testpw")

    def test_invalid_update(self):
        customer_payload = {
            "name": "John Doe",
            "email": "test@email.com",
            "password": "123"       
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.put('/customers/1', json=customer_payload, headers=headers)
        self.assertIn(response.status_code, [400, 401, 404])
        self.assertEqual(response.json['phone'], ['Missing data for required field.'])
        # self.assertIn('customer not found', response.get_data(as_text=True))
        # self.assertIn('missing token', response.get_data(as_text=True))
        # self.assertIn('token expired', response.get_data(as_text=True))
        # self.assertIn('invalid token', response.get_data(as_text=True))
        # self.assertIn('you must be logged in to access this.', response.get_data(as_text=True))

    # delete customer tests with token
    def test_delete_customer(self):
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.delete('/customers/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('succesfully deleted customer 1', response.get_data(as_text=True))

    def test_invalid_delete(self):
        response = self.client.delete('/customers/999')
        self.assertIn(response.status_code, [400, 401])
        # self.assertIn('missing token', response.get_data(as_text=True))
        # self.assertIn('token expired', response.get_data(as_text=True))
        # self.assertIn('invalid token', response.get_data(as_text=True))
        # self.assertIn('you must be logged in to access this.', response.get_data(as_text=True))
