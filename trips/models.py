from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from cloudinary.models import CloudinaryField
from .utils import get_coordinates


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
        created_on (DateTimeField): Date and time when the trip was created.
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
        related_name='trip'
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
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    trip_category = models.CharField(
        max_length=50,
        choices=TRIP_CATEGORY,
        default='LEISURE'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    trip_status = models.CharField(
        choices=TRIP_STATUS,
        default='PLANNED',
        max_length=50
    )
    shared = models.CharField(
        max_length=3,
        choices=SHARE_CHOICES,
        default='YES'
    )

    image = CloudinaryField(
        'image',
        default=None,
        blank=True
    )

    # Raise Validation Error In Model Save Method:
    # https://ilovedjango.com/django/models-and-databases/tips/sub/raise-validation-error-in-model-save-method/

    is_cleaned = False

    def clean(self):
        """
        Cleans the Trip instance by setting the `is_cleaned` attribute to True,
        geocoding the `place` attribute to obtain latitude and longitude coordinates,
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
        super(Trip, self).clean()

    def save(self, *args, **kwargs):
        """
        Override the save() method to to set the Lat and Lon values
        before saving.
        This method ensures that the instance is cleaned before saving by calling
        the full_clean() method if the instance has not been cleaned yet. After
        performing the cleaning, it calls the parent class's save() method to
        save the instance.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.is_cleaned:
            self.full_clean()
        super(Trip, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.trip_category} trip to {self.place}, {self.country}'

    class Meta:
        ordering = ["-created_on", 'country', 'start_date']


class Image(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images'
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='images'
    )
    # image = models.ImageField(upload_to='images/')
    title = models.CharField(
        max_length=50,
        blank=False,
        validators=[MinLengthValidator(2)])
    image = CloudinaryField(
        'image',
        default=None,
        blank=False
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
        return f'{self.trip.title}, {self.trip.place},\
                 {self.trip.country}'

    class Meta:
        ordering = ["-uploaded_at"]
