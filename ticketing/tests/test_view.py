from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

from ticketing.tests.test_basic import TestBase


class TestLogIn(TestBase):
    
    def setUp(self):
        super().setUp()
        
        
    def test_login(self):
        print(self.data.get('access'))
        print(self.token)
        self.assertEqual(self.response.status_code, 200)  
        self.assertIn("access", self.data)