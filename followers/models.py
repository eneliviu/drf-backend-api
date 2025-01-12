from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Follower(models.Model):
    """
    Represents a follower relationship between two users.
    Attributes:
        owner (ForeignKey): The user who is following another user.
        followed (ForeignKey): The user who is being followed.
        created_at (DateTimeField): The timestamp when the follow relationship
                                        was created.
    Methods:
        clean(): Validates that a user cannot follow themselves.
        save(*args, **kwargs): Saves the follower relationship
                                after validation.
    Meta:
        ordering (list): Orders the follower relationships by creation date in
                            descending order.
        unique_together (list): Ensures that a user cannot follow the
                                    same user more than once.
    Returns:
        str: A string representation of the follower relationship.
    """

    owner = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User,
        related_name='followed',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('owner', 'followed')

    def __str__(self):
        return f"{self.owner} follows {self.followed}"
