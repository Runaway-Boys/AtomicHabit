from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
User = get_user_model()
class LoginTest(TestCase):
    def setUp(self): 
        self.user_a = User.objects.create_user('homer',password='simpson') 

    def login_user(self):
        login = self.user_a.login(username='homer', password='simpson') 
        self.assertTrue(login) 


