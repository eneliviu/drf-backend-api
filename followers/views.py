from rest_framework import generics, permissions
from api.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer


class FollowerList(generics.ListCreateAPIView):
    """
    API view to retrieve list of followers or create a new follower.
    - GET: Returns a list of all followers.
    - POST: Creates a new follower with the authenticated user as the owner.
    Attributes:
        permission_classes (list): List of permission classes that determine
                                    access to the view.
        queryset (QuerySet): QuerySet of all Follower objects.
        serializer_class (Serializer): Serializer class to validate input,
                                        deserialize input, serialize output.
    Methods:
        perform_create(serializer): Saves the new follower instance with the
                                        authenticated user as the owner.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    FollowerDetail view for retrieving and deleting a follower instance.
    This view allows the owner of the follower model instance to retrieve
    or delete it.
    It uses the IsOwnerOrReadOnly permission class to ensure that only the
    owner can delete the follower instance, while others can only read it.
    Attributes:
        permission_classes (list): Permission classes that this view requires.
        queryset (QuerySet): The queryset that this view operates on.
        serializer_class (Serializer): The serializer class used for
                                        serializing the follower instances.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
