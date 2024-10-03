from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

from ticketing.tests.test_basic import TestBase


class TestLogIn(TestBase):
    
    def setUp(self):
        super().setUp()
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.url_get_ticket = reverse("detail_question",args=(("1",)))
        
    def test_login(self):
        self.assertEqual(self.response.status_code, 200)  
        self.assertIn("access", self.data)
        
    def test_get_ticket_answer(self):
        response = self.client.get(self.url_get_ticket,**self.headers)
        response_data = self.change_binary_to_dict(response.content)
        self.assertEqual(response_data,{'detail': 'Not found.'})