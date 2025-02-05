# this file is for creating test cases related to service tickets

# imports
from app.models import db, Service_Ticket, Customer
from app import create_app
import unittest
from datetime import datetime

# service ticket test cases
class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="test_customer", email="test@email.com", phone="1112223333", password='test')
        self.service_ticket = Service_Ticket(VIN="12345678901234567", service_date="2025-01-30", service_desc="tired", customer_id=1)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.add(self.service_ticket)
            db.session.commit()
        self.client = self.app.test_client()

    # create service ticket tests
    def test_create_service_ticket(self):
        service_ticket_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "2223334444",
            "password": "testpassword"
        }

        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_invalid_creation(self):
        service_ticket_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"       
        }

        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    # get all service ticket tests
    def test_get_service_tickets(self):
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)

    # get customer service tickets with token required tests
    def test_get_service_ticket_by_id(self):
        response = self.client.get('/service_tickets/1')
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_service_ticket_by_id(self):
        response = self.client.get('/service_tickets/999')
        self.assertEqual(response.status_code, 400)
        self.assertIn('invalid service_ticket id', response.get_data(as_text=True))

    # edit service ticket tests
    def test_update_service_ticket(self):
        update_payload = {
            "name": "Peter",
            "phone": "5558889999",
            "email": "test@email.com",
            "password": "testpw"
        }

        headers = {'Authorization': "Bearer " + self.test_login_service_ticket()}

        response = self.client.put('/service_tickets/1', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter') 
        self.assertEqual(response.json['email'], 'test@email.com')

    def test_invalid_update(self):
        service_ticket_payload = {
            "name": "John Doe",
            "email": "test@email.com",
            "password": "123"       
        }

        headers = {'Authorization': "Bearer " + self.test_login_service_ticket()}
        response = self.client.put('/service_tickets/1', json=service_ticket_payload, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['phone'], ['Missing data for required field.'])

    # add required parts tests
    def test_update_service_ticket(self):
        update_payload = {
            "name": "Peter",
            "phone": "5558889999",
            "email": "test@email.com",
            "password": "testpw"
        }

        headers = {'Authorization': "Bearer " + self.test_login_service_ticket()}

        response = self.client.put('/service_tickets/1', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter') 
        self.assertEqual(response.json['email'], 'test@email.com')

    def test_invalid_update(self):
        service_ticket_payload = {
            "name": "John Doe",
            "email": "test@email.com",
            "password": "123"       
        }

        headers = {'Authorization': "Bearer " + self.test_login_service_ticket()}
        response = self.client.put('/service_tickets/1', json=service_ticket_payload, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['phone'], ['Missing data for required field.'])
