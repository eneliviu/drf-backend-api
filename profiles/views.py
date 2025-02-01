from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class ProfileList(generics.ListAPIView):
    """
    API view to retrieve a list of profiles with annotated counts and
    filtering options.

    Attributes:
        serializer_class (ProfileSerializer): The serializer class used for
                                                the profiles.
        queryset (QuerySet): The queryset of profiles with annotated counts
                                for trips, images, likes, followers, and
                                following profiles.
        filter_backends (list): List of filter backends used for ordering and
                                    filtering the queryset.
        filterset_fields (list): List of fields that can be used for filtering
                                    the queryset.
        ordering_fields (list): List of fields that can be used for ordering
                                    the queryset.
    """
    serializer_class = ProfileSerializer

    queryset = Profile.objects.annotate(
        trips_count=Count('owner__trips', distinct=True),
        images_count=Count('owner__trips__images', distinct=True),
        likes_count=Count('owner__trips__images', distinct=True),
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
        'images_count',
        'followers_count',
        'following_count',
        'likes_count',
        'owner__following__created_at',
        'owner__followed__created_at'
        ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a profile instance.
    This view allows the owner of the profile to update or delete it, while
    other users can only read the profile details. The profile details include
    counts of trips, images, followers, and following.
    Attributes:
        permission_classes (list): List of permission classes that determine
            access to this view. Only the owner can update or delete a profile.
        serializer_class (ProfileSerializer): The serializer class used to
            serialize and deserialize profile instances.
        queryset (QuerySet): The queryset used to retrieve profile instances,
            annotated with counts of trips, images, followers, and following,
            and ordered by creation date in descending order.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        trips_count=Count('owner__trips', distinct=True),
        images_count=Count('owner__trips__images', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')


class ExtendedTokenObtainPairView(TokenViewBase):
    """
    Custom view for obtaining a pair of JWT tokens (access and refresh)
    using username and password.
    This view extends the TokenViewBase and uses the TokenObtainPairSerializer
    for token generation.
    It includes additional validation for username and password before
    attempting to generate tokens.

    Methods
    -------
    post(request, *args, **kwargs)
        Handles POST requests to obtain JWT tokens.
        Validates username and password before generating tokens.
    validate_username(username)
        Validates the provided username: checks if the username is not blank
        and exists in the database.
    validate_password(username, password)
        Validates the provided password: checks if the password is not blank
        and matches the username.
    """

    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        errors = {}
        errors.update(self.validate_username(username))
        errors.update(self.validate_password(username, password))

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def validate_username(self, username):
        errors = {}
        if not username:
            errors['username'] = ["This field may not be blank."]
        elif not User.objects.filter(username=username).exists():
            errors['username'] = ["This username does not exist."]
        return errors

    def validate_password(self, username, password):
        errors = {}
        if not password:
            errors['password'] = ["This field may not be blank."]
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                errors['password'] = ["The password is incorrect."]
        return errors