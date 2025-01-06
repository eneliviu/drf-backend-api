from django.db import models
from django.conf import settings


class Follower(models.Model):
    """
    Represents a follower relationship between two users.
    Attributes:
        owner (ForeignKey): The user who is following another user.
        followed_user (ForeignKey): The user who is being followed.
        created_at (DateTimeField): The timestamp when the follow relationship
            was created.
    Meta:
        ordering (list): Orders the follower relationships by creation date
            in descending order.
        unique_together (tuple): Ensures that a user cannot follow the same
            user more than once.
    Methods:
        __str__(): Returns a string representation of the follower
            relationship.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('owner', 'followed_user')

    def __str__(self):
        return f"{self.owner} follows {self.followed_user}"
