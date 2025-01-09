from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from likes.models import Like
from trips.models import Trip, Image
from django.contrib.auth.models import User


class LikeViewTests(TestCase):
    def setUp(self):
        '''
        Set up the test client and other test variables.
        '''
        self.admin = User.objects.create_user(username='admin', password='pass')

    def test_can_list_likes(self):
        admin = User.objects.get(username='admin')
        Trip.objects.create(owner=admin,
                            place='New York',
                            country='USA',
                            trip_category='Adventure',
                            start_date='2025-03-01',
                            end_date='2025-03-10',
                            trip_status='Planned',
                            shared=True)
        trip = Trip.objects.first()
        Image.objects.create(owner=admin,
                            trip=trip,
                            image='image.jpg',
                            image_title='image title')
        Like.objects.create(owner=admin, image=Image.objects.first())
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_can_create_like(self):
        admin = User.objects.get(username='admin')
        Trip.objects.create(owner=admin,
                            place='New York',
                            country='USA',
                            trip_category='Adventure',
                            start_date='2025-03-01',
                            end_date='2025-03-10',
                            trip_status='Planned',
                            shared=True)
        trip = Trip.objects.first()
        Image.objects.create(owner=admin,
                            trip=trip,
                            image='image.jpg',
                            image_title='image title')
        response = self.client.post('/likes/', {'owner': admin.id, 'image': Image.objects.first().id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)
        print(len(response.data))
