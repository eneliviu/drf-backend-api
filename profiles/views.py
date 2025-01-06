from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    API view to retrieve a list of profiles with dynamic ordering
    and filtering.
    Attributes:
        serializer_class (ProfileSerializer): Serializer class for
                                                profile data.
        permission_classes (list): Permission classes to apply to the view.
        filter_backends (list): List of filter backends to use for ordering
                                    and filtering.
        ordering_fields (list): List of fields that can be used for ordering
                                    the results.
    Methods:
        get_queryset(self):
            Retrieves the queryset of profiles with additional computed fields
            and optional filtering by owner username.
    """

    serializer_class = ProfileSerializer
    # queryset = Profile.objects.all()
    queryset = Profile.objects.annotate(
        trips_count=Count('owner__trip', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
        ]
    ordering_fields = [
        'trips_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at'
        ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a profile instance.
    Attributes:
        permission_classes (list): Permission classes required by the view.
        serializer_class (class): The serializer class that should be used for
                                    validating and deserializing input, and for
                                    serializing output.
        queryset (QuerySet): The queryset that should be used for retrieving
                                objects from the database.
                             Annotates each profile with:
                                - posts_count: No. of trips the user has.
                                - followers_count: No. profile followers.
                                - following_count: No. of profiles folowed
                             Orders the profiles by creation date in
                                descending order.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        trips_count=Count('owner__trip', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
