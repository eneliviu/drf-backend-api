from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class ProfilePageAccessTests(APITestCase):
    '''
    Test if users can access their profile page.
    '''
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='pass')
        self.client.login(username='admin', password='pass')

    def test_can_access_profile_page(self):
        response = self.client.get(f'/profiles/{self.user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
