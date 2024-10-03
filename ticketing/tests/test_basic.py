from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
import json
class TestBase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.username = 'testuser'
        self.password = 'testpassword'
        User = get_user_model()
        self.user = User.objects.create_user(self.username, password=self.password)
        self.anonymous_user = AnonymousUser
        post_data ={
                "username": self.username,
                "password": self.password
            }
        self.response = self.client.post(self.url, data=post_data)
        json_string = self.response.content.decode('utf-8')

        data = json.loads(json_string)
        self.data = json.loads(json_string)
        self.token = data.get('access')
        

    def change_binary_to_dict(self,binary_):
        json_string = binary_.decode('utf-8')
        data = json.loads(json_string)
        return data