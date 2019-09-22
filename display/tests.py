from django.test import TestCase
from django.urls import resolve, reverse
import json
from .models import Event,User
from django.test.utils import override_settings
from django.conf import settings
# Create your tests here.

class loginTest(TestCase):
    def setUp(self):
        self.name = 'loginTest'
        default_user = User()
        default_user.save()

    def test_login_false_case(self):
        url = reverse('login')
        response = self.client.post(path=url
                                    ,data={
                "username":"wrong",
                "password":"right",
            })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(eval(data['err']),1)

    def test_methon_err_case(self):
        url = reverse('login')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['err'], '3')

    def test_login_succeed_case(self):
        url = reverse('login')
        response = self.client.post(path=url
                                    , data={
                "username": "sadness",
                "password": "happiness",
            })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['success'], '0')

    def test_logout_false_case(self):
        logout = reverse('logout')
        response = self.client.post(path=logout)
        data = response.json()
        self.assertEqual(data['err'], '1')

    def test_logout_succeed_case(self):
        login = reverse('login')
        self.client.post(
            path=login,
            data={
                "username": "sadness",
                "password": "happiness",
            })

        logout = reverse('logout')
        response = self.client.post(path=logout)
        data = response.json()
        self.assertEqual(data['success'], '0')

class countTest(TestCase):
    def setUp(self):
        self.name = 'countTest'
        init = reverse('init')
        self.client.get(path=init)
        default_user = User()
        default_user.save()
        login = reverse('login')
        self.client.post(
            path=login,
            data={
                "username": "sadness",
                "password": "happiness",
            })

    def test_parameters_empty(self):
        response = self.client.get('http://127.0.0.1:8000/query/count')
        print(response.json())

    def test_parameters_1(self):
        response = self.client.get('http://127.0.0.1:8000/query/count?first_category=STREET_ID')
        print(response.json())

    def test_parameters_1_1(self):
        response = self.client.get('http://127.0.0.1:8000/query/count?first_category=STREET_ID&'
                                   'first_category_filter_id=100,101')
        print(response.json())

    def test_parameters_2(self):
        response = self.client.get('http://127.0.0.1:8000/query/count?first_category=STREET_ID&'
                                   'second_category=EVENT_PROPERTY_ID')
        print(response.json())

    def test_parameters_2_2(self):
        response = self.client.get('http://127.0.0.1:8000/query/count?first_category=STREET_ID&'
                                   'second_category=EVENT_PROPERTY_ID&second_category_filter_id=2,3')
        print(response.json())

    def test_parameters_time(self):
        response = self.client.get('http://127.0.0.1:8000/query/count?time_after=2018-09-01&time_before=2018-10-01')
        print(response.json())