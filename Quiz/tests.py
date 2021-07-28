from django.test import TestCase, Client
from django.urls import reverse
from requests.models import Request
from Quiz.models import *
# Create your tests here.

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        # self.

    def test_home(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'Quiz/Index.html')
    
    def test_logout(self):
        response = self.client.get(reverse('logout'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'Quiz/Index.html')

    def test_register_get(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response,'Quiz/Register.html')

    def test_register_post(self):
        response = self.client.post(reverse('register'))
        self.assertTemplateUsed(response,'Quiz/quizHome.html')

    def test_login_forbiden(self):
        response = self.client.post(reverse('login'))
        self.assertEquals(response.status_code,403)
    
    def test_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response,'Quiz/Error404.html')
    
    def test_submit(self):
        response = self.client.get(reverse('submit'))
        self.assertTemplateUsed(response,'Quiz/Result.html')

    def test_startQuiz_get(self):
        response = self.client.get(reverse('startQuiz'))
        self.assertTemplateUsed(response,'Quiz/Error404.html')
    
    def test_startQuiz_post(self):
        response = self.client.post(reverse('startQuiz'))
        self.assertTemplateUsed(response,'Quiz/Index.html')
