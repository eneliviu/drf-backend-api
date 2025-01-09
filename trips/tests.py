from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from .models import Trip, Image
from django.contrib.auth.models import User

'''
Test suite for the Trip and Image API endpoints.
This module contains test cases for the following views:
- TripListView: Tests for listing trips, including handling shared and non-shared trips.
- TripDetailView: Tests for retrieving a specific trip using valid and invalid IDs.
- ImageListView: Tests for listing images associated with trips, including handling shared and non-shared images.
- ImageDetailView: Tests for retrieving a specific image associated with a trip using valid and invalid IDs.
Classes:
    TripListViewTests(TestCase): Test suite for the TripListView.
    PostDetailViewTests(APITestCase): Test suite for the TripDetailView.
    TripImageListViewTests(TestCase): Test suite for the ImageListView.
    TripImageDetailViewTests(APITestCase): Test suite for the ImageDetailView.
Each test class contains setup methods to initialize test data and individual test methods to verify the functionality of the respective endpoints.
'''

class TripListViewTests(TestCase):
    """
    Test suite for the TripListView.
    This class contains tests to verify the functionality of listing trips
    through the TripListView endpoint. It includes tests for listing trips
    that are shared and handling trips that are not shared.
    """

    def setUp(self):
        '''
        Set up the test client and other test variables.
        '''
        self.admin = User.objects.create_user(username='admin', password='pass')

    def test_can_list_trips(self):
        '''
        Test to verify that the TripListView can list trips.
        '''
        admin = User.objects.get(username='admin')
        Trip.objects.create(owner=admin,
                            place='New York',
                            country='USA',
                            trip_category='Adventure',
                            start_date='2025-03-01',
                            end_date='2025-03-10',
                            trip_status='Planned',
                            shared=True)
        response = self.client.get('/trips/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_can_handle_list_trips_not_shared(self):
        '''
        Test to verify that the TripListView can handle trips that are not shared.
        '''
        admin = User.objects.get(username='admin')
        Trip.objects.create(owner=admin,
                            place='New York',
                            country='USA',
                            trip_category='Adventure',
                            start_date='2025-03-01',
                            end_date='2025-03-10',
                            trip_status='Planned',
                            shared=False)
        response = self.client.get('/trips/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))


class PostDetailViewTests(APITestCase):
    '''
    Test suite for the TripDetailView.
    This class contains tests to verify the functionality of retrieving a trip
    through the TripDetailView endpoint. It includes tests for retrieving a trip
    using a valid and an invalid id.
    '''
    def setUp(self):
        '''
        Set up the test client and other test variables.
        '''
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin', password='pass')
        Trip.objects.create(owner=self.admin,
                            place='New York',
                            country='USA',
                            trip_category='Adventure',
                            start_date='2025-03-01',
                            end_date='2025-03-10',
                            trip_status='Planned',
                            shared=True)

    def test_can_retrieve_post_using_valid_id(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get('/trips/1/')  # retrieve post
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_retrieve_post_using_invalid_id(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get('/trips/999/')  # retrieve post
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TripImageListViewTests(TestCase):
    '''
    Test suite for the ImageListView.
    This class contains tests to verify the functionality of listing images
    through the ImageListView endpoint. It includes tests for listing images
    that are shared and handling images that are not shared.
    '''
    def setUp(self):
        '''
        Set up the test client and other test variables.
        '''
        self.admin = User.objects.create_user(username='admin', password='pass')

    def test_can_list_trip_images(self):
        '''
        Test to verify that the ImageListView can list images.
        '''
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

        response = self.client.get('/trips/1/images/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_can_handle_list_trip_images_not_shared(self):
        '''
        Test to verify that the ImageListView can handle images that are not shared.
        '''
        admin = User.objects.get(username='admin')
        Trip.objects.create(owner=admin,
                            place='New York',
                            country='USA',
                            trip_category='Adventure',
                            start_date='2025-03-01',
                            end_date='2025-03-10',
                            trip_status='Planned',
                            shared=False)
        trip = Trip.objects.first()
        Image.objects.create(owner=admin,
                            trip=trip,
                            image='image.jpg',
                            image_title='image title')

        response = self.client.get('/trips/1/images/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))


class TripImageDetailViewTests(APITestCase):
    '''
    Test suite for the ImageDetailView.
    This class contains tests to verify the functionality of retrieving an image
    through the ImageDetailView endpoint. It includes tests for retrieving an image
    using a valid and an invalid id.
    '''
    def setUp(self):
        '''
        Set up the test client and other test variables.
        '''
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin', password='pass')
        Trip.objects.create(owner=self.admin,
                            place='New York',
                            country='USA',
                            trip_category='Adventure',
                            start_date='2025-03-01',
                            end_date='2025-03-10',
                            trip_status='Planned',
                            shared=True)
        trip = Trip.objects.first()
        Image.objects.create(owner=self.admin,
                            trip=trip,
                            image='image.jpg',
                            image_title='image title')

    def test_can_retrieve_trip_image_using_valid_id(self):
        '''
        Test to verify that the ImageDetailView can retrieve an image.
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.get('/trips/1/images/1/')  # retrieve image
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_retrieve_trip_image_using_invalid_id(self):
        '''
        Test to verify that the ImageDetailView can handle an invalid image id.
        '''
        self.client.login(username='admin', password='pass')
        response = self.client.get('/trips/1/images/999/')  # retrieve image
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)