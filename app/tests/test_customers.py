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
        print("PRINTING")
        print(response.json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"       
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

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
        self.assertEqual(response.status_code, 400)
        self.assertIn('invalid customer id', response.get_data(as_text=True))
    
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
        self.assertEqual(response.json['name'], 'Peter') 
        self.assertEqual(response.json['email'], 'test@email.com')

    def test_invalid_update(self):
        customer_payload = {
            "name": "John Doe",
            "email": "test@email.com",
            "password": "123"       
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.put('/customers/1', json=customer_payload, headers=headers)
        self.assertEqual(response.status_code, 400)
        print(response.json)
        self.assertEqual(response.json['phone'], ['Missing data for required field.'])

    # delete customer tests with token
    def test_delete_customer(self):
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.delete('/customers/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('succesfully deleted customer 1', response.get_data(as_text=True))

    def test_invalid_delete(self):
        response = self.client.delete('/customers/999')
        self.assertEqual(response.status_code, 400)
        self.assertIn('You must be logged in to access this.', response.get_data(as_text=True))
