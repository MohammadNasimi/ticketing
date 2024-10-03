from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

from ticketing.tests.test_basic import TestBase
from ticketing.views import UpdateTicktetView


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
        
class TestRequest(TestBase):
    
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        
    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get("ticketing/ticketanswer/detail/1/")

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        # request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = self.user
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        print(request)
        # Test function view() -->  response = UpdateTicktetView(request) 
        # Use this syntax for class-based views.
        response = UpdateTicktetView.as_view()(request)
        self.assertEqual(401, 401)
        