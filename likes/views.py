from rest_framework import generics, permissions
from api.permissions import IsOwnerOrReadOnly
from likes.models import Like
from likes.serializers import LikeSerializer


# Create your views here.
class LikeList(generics.ListCreateAPIView):
    """
    API view to retrieve list of likes or create a new like.
    - GET: Returns a list of all likes.
    - POST: Creates a new like. Only authenticated users can post likes.
    Attributes:
        permission_classes (list): Permission classes for access to the view.
        serializer_class (LikeSerializer): Serializer class used to validate
                                                and serialize data.
        queryset (QuerySet): QuerySet of all Like objects.
    Methods:
        perform_create(serializer):
            Sets the user creating the like as its owner.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    API view to retrieve or delete a Like instance.
    This view allows the owner of the Like instance to retrieve or delete it.
    Other users can only read the Like instance.
    Attributes:
        permission_classes (list): Permission classes required.
        serializer_class (class): Serializer to validate and serialize data.
        queryset (QuerySet): The base queryset for retrieving Like instances.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
