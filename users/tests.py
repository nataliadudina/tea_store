from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from django.test import TestCase


class RegisterUserTestCase(TestCase):

    def setUp(self):
        self.data = {
            'username': 'user_1',
            'email': 'user1@gmail.com',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }

    def test_form_registration_get(self):
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_success(self):
        user_model = get_user_model()

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:activation_sent'))
        self.assertTrue(user_model.objects.filter(email=self.data['email']).exists())

    def test_user_registration_password_error(self):
        self.data['password2'] = '12345678A'

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "The two password fields didn’t match")

    def test_user_registration_user_exists_error(self):
        user_model = get_user_model()
        user_model.objects.create(email=self.data['email'])

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "This email already exists.")
