from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from cloudinary.models import CloudinaryField
from .utils import get_coordinates, validate_image


class Trip(models.Model):
    """
    Model representing a trip.
    Attributes:
        owner (ForeignKey): The user who owns the trip.
        place (CharField): The place of the trip.
        country (CharField): The country of the trip.
        lat (FloatField): The latitude of the trip location.
        lon (FloatField): The longitude of the trip location.
        trip_category (CharField): The category of the trip.
        start_date (DateField): The start date of the trip.
        end_date (DateField): The end date of the trip.
        created_at (DateTimeField): Date and time when the trip was created.
        trip_status (CharField): The status of the trip.
        shared (CharField): Indicates if the trip is shared.
        image (CloudinaryField): An image associated with the trip.
        coordinates (CharField): The coordinates of the trip location.
        is_cleaned (bool): Indicates if the model has been cleaned.
    Methods:
        clean(): Cleans the model instance and sets latitude and longitude.
        save(*args, **kwargs): Overrides the save method to ensure the model
                                data is cleaned before saving.
        __str__(): Returns a string representation of the trip.
    """

    TRIP_CATEGORY = (('Leisure', 'LEISURE'),
                     ('Business', 'BUSINESS'),
                     ('Adventure', 'ADVENTURE'),
                     ('Family', 'FAMILY'),
                     ('Romantic', 'ROMANTIC'))
    TRIP_STATUS = (("Completed", 'COMPLETED'),
                   ("Ongoing", "ONGOING"),
                   ("Planned", 'PLANNED'))
    SHARE_CHOICES = (("Yes", "YES"),
                     ("NO", 'No'))

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trips'
    )

    title = models.CharField(
        max_length=100,
        blank=False,
        validators=[MinLengthValidator(2)]
        )

    place = models.CharField(
        max_length=100,
        blank=False,
        validators=[MinLengthValidator(2)]
        )
    country = models.CharField(
        max_length=100,
        blank=False,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(56)
            ]
        )
    content = models.TextField(
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(500)
            ]
        )
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    trip_category = models.CharField(
        max_length=50,
        choices=TRIP_CATEGORY,
        default='LEISURE'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    trip_status = models.CharField(
        choices=TRIP_STATUS,
        default='PLANNED',
        max_length=50
    )
    shared = models.BooleanField(default=True)

    is_cleaned = False

    def clean(self):
        """
        Cleans the Trip instance by setting the `is_cleaned` attribute to True,
        geocoding the `place` attribute to obtain latitude and longitude,
        and raising a ValidationError if the geocoding fails.
        Raises:
            ValidationError: If the geocoding of the `place` attribute fails.
        """
        self.is_cleaned = True
        coords = get_coordinates(self.place)

        if coords == 'location-error':
            raise ValidationError("Error: could not geocode the location")
        else:
            self.lat = coords[0]
            self.lon = coords[1]

        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")

        super().clean()

    def save(self, *args, **kwargs):
        """
        Override the save() method to to set the Lat and Lon values
        before saving.
        This method ensures that the instance is cleaned before saving by
        calling the full_clean() method if the instance has not been cleaned.
        After performing the cleaning, it calls the parent class's save()
        method to save the instance.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.is_cleaned:
            self.full_clean()
        super(Trip, self).save(*args, **kwargs)

    def __str__(self):
        return (f'{self.trip_category} trip to {self.place}, '
                f'{self.country}, '
                f'by {self.owner.username}, '
                f'from {self.start_date} to {self.end_date}')

    class Meta:
        ordering = ["-created_at", 'country', 'start_date']


class Image(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image_title = models.CharField(
        max_length=50,
        blank=False,
        validators=[MinLengthValidator(2)])

    image = CloudinaryField(
        'image',
        default='https://res.cloudinary.com/dchoskzxj/image/upload/'
                'v1721990160/yg9qwd4v15r23bxwv5u4.jpg',
        blank=True,
        null=True,
        validators=[validate_image]
    )

    description = models.TextField(
        blank=False,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(500)
            ]
        )

    shared = models.BooleanField(default=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_uploaded_at = self.uploaded_at.strftime('%Y-%m-%d %H:%M')
        return (
            f'From {self.trip.place}, '
            f'{self.trip.country}, '
            f'uploaded at {formatted_uploaded_at}, '
            f'by {self.owner.username}'
        )

    class Meta:
        ordering = ["-uploaded_at", "owner"]

    def save(self, *args, **kwargs):
        """
        Overrides the save method to include image validation.
        If the instance already exists (has a primary key), it validates
            the new image only if it has changed.
        If the instance is new (does not have a primary key),
            it validates the image.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Raises:
            ValidationError: If the image does not pass validation.
        """

        if self.pk:
            old_image = Image.objects.get(pk=self.pk).image
            if old_image != self.image:
                validate_image(self.image)
        else:
            validate_image(self.image)
        super(Image, self).save(*args, **kwargs)
