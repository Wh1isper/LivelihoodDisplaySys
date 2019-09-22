from django.test import TestCase
from django.urls import resolve, reverse
import json
from .models import Event,User
# Create your tests here.

class loginTest(TestCase):
    def setUp(self):
        self.name = 'Django'

    def test_login_false_case(self):
        default_user = User()
        default_user.save()
        url = reverse('login')
        response = self.client.post(path=url
                                    ,data={
                "username":"wrong",
                "password":"right",
            })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(eval(data['err']),1)

    def test_request_err_case(self):
        default_user = User()
        default_user.save()
        url = reverse('login')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(eval(data['err']), 1)

    def test_login_succeed_case(self):
        default_user = User()
        default_user.save()
        url = reverse('login')
        response = self.client.post(path=url
                                    , data={
                "username": "sadness",
                "password": "happiness",
            })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['msg'], 'login')

    def test_logout_false_case(self):
        logout = reverse('logout')
        response = self.client.post(path=logout)
        data = response.json()
        self.assertEqual(data['err'], '1')

    def test_logout_succeed_case(self):
        default_user = User()
        default_user.save()
        login = reverse('login')
        self.client.post(path=login
                                    , data={
                "username": "sadness",
                "password": "happiness",
            })

        logout = reverse('logout')
        response = self.client.post(path=logout)
        data = response.json()
        self.assertEqual(data['msg'],'logout')

