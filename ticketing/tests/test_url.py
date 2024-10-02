from django.test import SimpleTestCase
from django.urls import resolve,reverse,reverse_lazy

class TestUrl(SimpleTestCase):
    
    def test_ticket_list(self):
        url = reverse('create_question')
        url1 = reverse_lazy('create_question')
        view_class = resolve(url).func.view_class
        self.assertTrue(url,view_class)
        
    def test_ticket_list(self):
        url = reverse('create_answer',args=("1", ))
        url1 = reverse_lazy('create_answer')
        view_class = resolve(url).func.view_class
        self.assertTrue(url,view_class)