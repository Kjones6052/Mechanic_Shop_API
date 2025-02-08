# this file is for creating test cases related to service tickets

# imports
from app.models import db, Service_Ticket, Customer, Mechanic, Part
from app import create_app
import unittest
from datetime import datetime

# service ticket test cases
class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.date = datetime.strptime("2025-01-24", "%Y-%m-%d").date()
        self.part = Part(part_name="tire", price=100.00)
        self.mechanic1 = Mechanic(name="joe mechanic", email="test1@email.com", phone="4445557777", salary=100.00)
        self.mechanic2 = Mechanic(name="mechanic bob", email="test2@email.com", phone="4448887777", salary=150.00)
        self.customer = Customer(name="test_customer", email="test3@email.com", phone="1112223333", password='test')
        self.service_ticket = Service_Ticket(VIN="12345678901234567", service_date=self.date, service_desc="tires", customer_id=1)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.add(self.mechanic1)
            db.session.add(self.mechanic2)
            db.session.add(self.service_ticket)
            db.session.commit()
        self.client = self.app.test_client()

    # customer login for access to token in later tests
    def test_login_customer(self):
        credentials = {
            "email": "test3@email.com",
            "password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']

    # create service ticket tests
    def test_create_service_ticket(self):
        service_ticket_payload = {
            "VIN": "11122233344455577",
            "service_date": self.date.strftime('%Y-%m-%d'),
            "service_desc": "tires",
            "customer_id": 1,
            "mechanic_ids": [1]
        }

        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['service_desc'], "tires")

    def test_invalid_creation(self):
        service_ticket_payload = {
            "VIN": "11122233344455577",
            "service_date": self.date,
            "service_desc": "tires",
            "mechanic_ids": [1]       
        }

        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json['customer_id'], ['Missing data for required field.'])

    # get all service ticket tests
    def test_get_service_tickets(self):
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)

    # get customer service tickets with token required tests
    def test_get_service_ticket_by_id(self):
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.get('/service_tickets/1/my_tickets', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_service_ticket_by_id(self):
        response = self.client.get('/service_tickets/999/my_tickets')
        self.assertEqual(response.status_code, 400)

    # edit mechanics on service ticket tests
    def test_edit_mechanics_service_ticket(self):
        edit_mechanics_payload = {
            "add_mechanic_ids": [1],
            "remove_mechanic_ids": [2]
        }

        response = self.client.put('/service_tickets/1/edit', json=edit_mechanics_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['VIN'], '12345678901234567') 
        self.assertEqual(response.json['service_desc'], 'tires')

    def test_invalid_edit_mechanics_service_ticket(self):
        edit_mechanics_payload = {
            "add_mechanic_ids": 1       
        }

        response = self.client.put('/service_tickets/1/edit', json=edit_mechanics_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['remove_mechanic_ids'], ['Missing data for required field.'])

    # add required parts to service ticket tests
    def test_add_parts_service_ticket(self):
        part_payload = {
            "ticket_id": 1,
            "part_id": 1,
            "quantity": 1
        }

        response = self.client.put('/service_tickets/1/add_part', json=part_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['required_parts'][0]['part_id'], 1)

    def test_invalid_add_parts(self):
        part_payload = {
            "part_id": 1,
            "quantity": 1       
        }

        response = self.client.put('/service_tickets/1/add_part', json=part_payload)
        print("\nPRINTING: add parts\n",response.json)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['ticket_id'], ['Missing data for required field.'])
