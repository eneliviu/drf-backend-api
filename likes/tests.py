from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from likes.models import Like
from trips.models import Trip, Image


class LikeViewTests(TestCase):
    def setUp(self):
        '''
        Set up the test client and other test variables.
        '''
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='pass'
        )

        self.trip = Trip.objects.create(
            title='Test Trip',
            owner=self.user,
            place='Test Place',
            country='Test Country',
            trip_category='Adventure',
            start_date='2025-03-01',
            end_date='2025-03-10',
            trip_status='Planned',
            shared=True
        )

    def test_can_list_likes(self):
        admin = User.objects.get(username='admin')
        Trip.objects.create(
            owner=admin,
            title='New York Trip',
            place='New York',
            country='USA',
            trip_category='Adventure',
            start_date='2025-03-01',
            end_date='2025-03-10',
            trip_status='Planned',
            shared=True
        )
        trip = Trip.objects.first()
        Image.objects.create(
            owner=admin,
            trip=trip,
            image=(
                'https://res.cloudinary.com/dchoskzxj/image/upload/'
                'v1721990160/yg9qwd4v15r23bxwv5u4.jpg'
            ),
            image_title='image title'
        )
        # image = Image.objects.create(
        #     owner=self.user,
        #     trip=self.trip,
        #     image_title='Valid Image',
        #     image=(
        #         'https://res.cloudinary.com/dchoskzxj/image/upload/'
        #         'v1721990160/yg9qwd4v15r23bxwv5u4.jpg'
        #     ),
        #     description='A valid image description.'
        # )
        Like.objects.create(
            owner=admin,
            image=Image.objects.first()
        )
        response = self.client.get('/likes/')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_can_create_like(self):
        admin = User.objects.get(username='admin')
        Trip.objects.create(
            title='New York Trip',
            owner=admin,
            place='New York',
            country='USA',
            trip_category='Adventure',
            start_date='2025-03-01',
            end_date='2025-03-10',
            trip_status='Planned',
            shared=True
        )
        trip = Trip.objects.first()
        image = Image.objects.create(
            owner=admin,
            trip=trip,
            image=(
                'https://res.cloudinary.com/dchoskzxj/image/upload/'
                'v1721990160/yg9qwd4v15r23bxwv5u4.jpg'
            ),
            image_title='image title'
        )
        
        # Authenticate the client
        self.client.force_authenticate(user=admin)
        
        # Create the like with the image ID
        response = self.client.post(
            '/likes/',
            {
                'owner': admin.id,
                'image': image.id  # Use the image ID, not the image object
            }
        )
        
        # Check the response status code
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )