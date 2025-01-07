from django.db import models
from django.contrib.auth.models import User
from trips.models import Image


# Create your models here.
class Like(models.Model):
    """
    Represents a 'Like' given by a user to an image.
    Attributes:
        owner (ForeignKey): A reference to the User who liked the post.
        image (ForeignKey): A reference to the Image that was liked.
        created_at (DateTimeField): The timestamp when the like was created.
    Meta:
        ordering (list): Orders the likes by creation date in descending order.
        unique_together (list): Ensures that a user can only like a specific
                                    image once.
    Methods:
        __str__(): Returns a string representation of the like, showing the
                    owner and the image title.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner',  'image']

    def __str__(self):
        """
        Returns a string representation of the Like instance.
        If the image has a title, it returns the owner's name followed by
        'liked' and the image title. If the image does not have a title,
        it returns the owner's name followed by 'liked "Untitled Image"'.
        Returns:
            str: A string representation of the like instance.
        """
        image_title = (
            self.image.image_title
            if self.image.image_title else "Untitled Image"
        )
        return f'{self.owner} liked {image_title}'
