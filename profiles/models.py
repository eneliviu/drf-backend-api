import os
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


def validate_image(image):
    """
    Validate the uploaded image file.
    This function checks the file extension of the uploaded image to ensure
    that it is one of the allowed types: .jpg, .jpeg, .png, .gif, .webp.
    If the file extension is not supported, a ValidationError is raised.
    Args:
        image (File): The uploaded image file.
    Raises:
        ValidationError: If the file extension is not supported.
    """

    file_extension = os.path.splitext(image.name)[1].lower()
    if file_extension not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        raise ValidationError("Unsupported file extension.")


class Profile(models.Model):
    """
    Profile model that represents a user's profile.
    Attributes:
        owner (User): A one-to-one relationship with the User model.
                      The profile is deleted if the associated user is deleted.
        created_at (datetime): The date and time when the profile was created.
                               Automatically set when the profile is created.
        updated_at (datetime): Date and time when the profile was last updated.
                               Automatically set when the profile is updated.
        name (str): An optional field for the profile's name.
                    Maximum length is 50 characters.
        content (str): Optional field for additional profile content.
        image (CloudinaryField): An optional field for the profile's image.
                                 Defaults to a specified URL if not provided.
                                 Validates the image using the `validate_image`
                                 function.
    Meta:
        ordering (list): Orders profiles by the `created_at` field
                            in descending order.
    Methods:
        __str__(): Returns a string representation of the profile,
                   typically the owner's name followed by "'s profile".
    """
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50, blank=True)
    alias = models.CharField(max_length=50, blank=True)
    content = models.TextField(blank=True)
    image = CloudinaryField(
        'image',
        default='https://res.cloudinary.com/dchoskzxj/image/upload/'
                'v1721990160/yg9qwd4v15r23bxwv5u4.jpg',
        blank=True,
        null=True,
        validators=[validate_image]
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a Profile instance whenever a
    new User instance is created.
    Args:
        sender (Model class): The model class that sent the signal.
        instance (Model instance): The actual instance being saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.
    Returns:
        None
    """
    if created:
        Profile.objects.create(owner=instance)
