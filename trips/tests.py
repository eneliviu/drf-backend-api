from django.test import TestCase, TransactionTestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Trip, Image

"""
Test suite for the Trip and Image API endpoints.
This module contains test cases for the following views:
- TripListView: Tests for listing trips, including handling shared and
    non-shared trips.
- TripDetailView: Tests for retrieving a specific trip using valid and
    invalid IDs.
- ImageListView: Tests for listing images associated with trips,
    including handling shared and non-shared images.
- ImageDetailView: Tests for retrieving a specific image associated with
    a trip using valid and invalid IDs.
- Image model: Tests for the Image model, including creating and updating
    images with valid and invalid data.
- Image model validation: Tests for validating the Image model's save method
    to ensure that it correctly validates new and updated images, particularly
    focusing on the validation of the image file extension.

Classes:
    TripListViewTests(TestCase): Test suite for the TripListView.
    PostDetailViewTests(APITestCase): Test suite for the TripDetailView.
    TripImageListViewTests(TestCase): Test suite for the ImageListView.
    TripImageDetailViewTests(APITestCase): Test suite for the ImageDetailView.
    ImageModelTests(TestCase): Test suite for the Image model.
    ImageModelValidationTests(TransactionTestCase): Test case for validating
        the Image model.

Each test class contains setup methods to initialize test data and individual
    test methods to verify the functionality of the respective endpoints.
"""


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
        self.admin = User.objects.create_user(
            username='admin',
            password='pass'
        )

    def test_can_list_trips(self):
        '''
        Test to verify that the TripListView can list trips.
        '''
        admin = User.objects.get(username='admin')
        Trip.objects.create(
            title='New York',
            owner=admin,
            place='New York',
            country='USA',
            trip_category='Adventure',
            start_date='2025-03-01',
            end_date='2025-03-10',
            trip_status='Planned',
            shared=True
        )
        response = self.client.get('/trips/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_can_handle_list_trips_not_shared(self):
        '''
        Test to verify that the TripListView can handle trips
        that are not shared.
        '''
        admin = User.objects.get(username='admin')
        Trip.objects.create(
            title='New York',
            owner=admin,
            place='New York',
            country='USA',
            trip_category='Adventure',
            start_date='2025-03-01',
            end_date='2025-03-10',
            trip_status='Planned',
            shared=False
        )
        response = self.client.get('/trips/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))


class TripDetailViewTests(APITestCase):
    '''
    Test suite for the TripDetailView.
    This class contains tests to verify the functionality of retrieving a trip
    through the TripDetailView endpoint. It includes tests for retrieving
    a trip using a valid and an invalid id.
    '''
    def setUp(self):
        '''
        Set up the test client and other test variables.
        '''
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            password='pass'
        )
        Trip.objects.create(
            title='New York',
            owner=self.admin,
            place='New York',
            country='USA',
            trip_category='Adventure',
            start_date='2025-03-01',
            end_date='2025-03-10',
            trip_status='Planned',
            shared=True
        )

    def test_can_retrieve_post_using_valid_id(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get('/trips/1/')  # retrieve post
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_retrieve_post_using_invalid_id(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get('/trips/999/')  # retrieve post
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TripImageListViewTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            password='pass'
        )

    def test_can_list_trip_images(self):
        admin = User.objects.get(username='admin')
        trip = Trip.objects.create(
            title='New York',
            owner=admin,
            place='New York',
            country='USA',
            trip_category='Adventure',
            start_date='2025-03-01',
            end_date='2025-03-10',
            trip_status='Planned',
            shared=True
        )
        Image.objects.create(
            owner=admin,
            trip=trip,
            image='image.jpg',  # Ensure this is a valid image path or URL
            image_title='image title'
        )

        response = self.client.get('/trips/1/images/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_can_handle_list_trip_images_not_shared(self):
        admin = User.objects.get(username='admin')
        trip = Trip.objects.create(
            title='New York',
            owner=admin,
            place='New York',
            country='USA',
            trip_category='Adventure',
            start_date='2025-03-01',
            end_date='2025-03-10',
            trip_status='Planned',
            shared=False
        )
        Image.objects.create(
            owner=admin,
            trip=trip,
            image='image.jpg',  # Ensure this is a valid image path or URL
            image_title='image title'
        )

        response = self.client.get('/trips/1/images/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))


class TripImageDetailViewTests(APITestCase):
    '''
    Test suite for the ImageDetailView.
    This class contains tests to verify the functionality of
    retrieving an image through the ImageDetailView endpoint.
    It includes tests for retrieving an image using a valid and an invalid id.
    '''
    def setUp(self):
        '''
        Set up the test client and other test variables.
        '''
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            password='pass'
        )
        Trip.objects.create(
            title='New York',
            owner=self.admin,
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
            owner=self.admin,
            trip=trip,
            image='image.jpg',
            image_title='image title'
        )

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


class ImageModelTests(TestCase):
    '''
    Test suite for the Image model including the following tests:
    - Setting up test data for the Image model.
    - Creating an Image instance with valid data.
    - Creating an Image instance with an invalid image file extension.
    - Updating an Image instance with a new valid image.
    - Updating an Image instance with an invalid image file extension.
    - Testing the __str__ method of the Image model.
    '''

    def setUp(self):
        """
        Set up test data.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
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

    def test_create_image_with_valid_data(self):
        """
        Test creating an Image instance with valid data.
        """
        image = Image.objects.create(
            owner=self.user,
            trip=self.trip,
            image_title='Valid Image',
            image=(
                'https://res.cloudinary.com/dchoskzxj/image/upload/'
                'v1721990160/yg9qwd4v15r23bxwv5u4.jpg'
            ),
            description='A valid image description.'
        )
        self.assertEqual(image.image_title, 'Valid Image')
        self.assertEqual(image.trip, self.trip)
        self.assertEqual(image.owner, self.user)

    def test_create_image_with_invalid_image_extension(self):
        """
        Test creating an Image instance with an invalid image file extension,
        e.g., .pdf.
        """
        with self.assertRaises(ValidationError):
            image = Image(
                owner=self.user,
                trip=self.trip,
                image_title='Invalid Image',
                image='image.pdf',
                description='An invalid image description.'
            )
            image.full_clean()  # Trigger validation

    def test_update_image_with_valid_image(self):
        """
        Test updating an Image instance with a new valid image.
        """
        image = Image.objects.create(
            owner=self.user,
            trip=self.trip,
            image_title='Original Image',
            image=(
                'https://res.cloudinary.com/dchoskzxj/image/upload/'
                'v1721990160/yg9qwd4v15r23bxwv5u4.jpg'
                ),
            description='Original description.'
        )
        image.image = (
            'https://res.cloudinary.com/dchoskzxj/image/'
            'upload/v1721990160/valid_image.png'
        )
        image.save()
        self.assertEqual(
            image.image,
            ('https://res.cloudinary.com/dchoskzxj/image/'
             'upload/v1721990160/valid_image.png')
        )

    def test_update_image_with_invalid_image_extension(self):
        """
        Test updating an Image instance with an invalid image file extension.
        """
        image = Image.objects.create(
            owner=self.user,
            trip=self.trip,
            image_title='Original Image',
            image=(
                'https://res.cloudinary.com/dchoskzxj/image/'
                'upload/v1721990160/yg9qwd4v15r23bxwv5u4.jpg'
            ),
            description='Original description.'
        )
        with self.assertRaises(ValidationError):
            image.image = 'https://example.com/invalid.pdf'
            image.full_clean()

    def test_image_str_method(self):
        """
        Test the __str__ method of the Image model.
        """
        image = Image.objects.create(
            owner=self.user,
            trip=self.trip,
            image_title='Test Image',
            image=(
                'https://res.cloudinary.com/dchoskzxj/image/'
                'upload/v1721990160/yg9qwd4v15r23bxwv5u4.jpg'
            ),
            description='Test description.'
        )
        expected_str = (
            f'From {self.trip.place}, '
            f'{self.trip.country}, '
            f'uploaded at {image.uploaded_at.strftime("%Y-%m-%d %H:%M")}, '
            f'by {self.user.username}'
        )
        self.assertEqual(str(image), expected_str)


class ImageModelValidationTests(TransactionTestCase):
    '''
    Test case for validating the Image model.
    This test case includes tests to ensure that the Image model's save method
    correctly validates new and updated images, particularly focusing on the
    validation of the image file extension.
    Methods
    -------
    setUp():
        Sets up the test data required for the tests.
    test_save_method_validates_new_image():
        Tests that the save method raises a ValidationError for a new image
        with an invalid extension.
    test_save_method_validates_updated_image():
        Tests that the save method raises a ValidationError for an updated
        image with an invalid extension.
    '''

    def setUp(self):
        """
        Set up test data.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.trip = Trip.objects.create(
            title='Test Trip',
            owner=self.user,
            place='Test Place',
            country='Test Country',
            trip_category='Adventure',
            start_date='2025-01-01',
            end_date='2025-01-10',
            trip_status='Planned',
            shared=True
        )

    def test_save_method_validates_new_image(self):
        """
        Test that the save method validates a new image.
        """
        with self.assertRaises(ValidationError):
            image = Image(
                owner=self.user,
                trip=self.trip,
                image_title='Invalid Image',
                image='https://example.com/invalid.pdf',
                description='An invalid image description.'
            )
            image.save()  # Should raise ValidationError

    def test_save_method_validates_updated_image(self):
        """
        Test that the save method validates an updated image.
        """
        image = Image.objects.create(
            owner=self.user,
            trip=self.trip,
            image_title='Original Image',
            image=(
                'https://res.cloudinary.com/dchoskzxj/image/'
                'upload/v1721990160/yg9qwd4v15r23bxwv5u4.jpg'
            ),
            description='Original description.'
        )
        with self.assertRaises(ValidationError):
            image.image = 'https://example.com/invalid.pdf'
            image.save()
