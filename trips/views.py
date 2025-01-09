from django.db.models import Count
from django_filters import (
    FilterSet, DateFilter, CharFilter, MultipleChoiceFilter, BooleanFilter
)
from rest_framework import generics, filters
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsOwnerOrReadOnly
from .models import Trip, Image
from .serializers import TripSerializer, ImageSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q


class TripFilter(FilterSet):
    """
    A filter set for filtering Trip objects based on various criteria.
    Attributes:
        owner__username (CharFilter): Filter trips by the owner's username.
        country (CharFilter): Filter trips by country.
        place (CharFilter): Filter trips by place.
        liked_by_user (BooleanFilter): Filter trips liked by the current user.
        user_trips (BooleanFilter): Filter trips by the user's profile.
        current_user_trips (BooleanFilter): Filter trips owned by the user.
        followed_users (BooleanFilter): Filter trips by users followed by
                                            the current user.
        trip_category (MultipleChoiceFilter): Filter trips by category.
        trip_status (MultipleChoiceFilter): Filter trips by status.
        trip_shared (MultipleChoiceFilter): Filter trips by shared status.
        start_date (DateFilter): Filter trips starting from a specific date.
        end_date (DateFilter): Filter trips ending by a specific date.
    Methods:
        filter_current_user_trips(queryset, name, value):
            Filters trips to include only those owned by the current user if
                the user is authenticated.
        filter_liked_by_user(queryset, name, value):
            Filters trips to include only those liked by the current user if
                the user is authenticated.
        filter_post_by_profile(queryset, name, value):
            Filters trips by the owner's profile.
        filter_followed_users(queryset, name, value):
            Filters trips to include only those owned by users followed by the
                current user if the user is authenticated.
        __init__(*args, **kwargs):
            Initializes the filter set and sets the owner's username to the
                current user's username if not provided.
    """

    owner__username = CharFilter(field_name='owner__username')
    country = CharFilter(field_name='country')
    place = CharFilter(field_name='place')

    liked_by_user = BooleanFilter(
        method='filter_liked_by_user',
        field_name='liked'
    )
    user_trips = BooleanFilter(
        method='filter_trip_by_profile',
        field_name='user_trips'
    )
    current_user_trips = BooleanFilter(
        method='filter_current_user_trips',
        field_name='current_user_trips'
    )
    followed_users = BooleanFilter(
        method='filter_followed_users',
        field_name='followed_users'
    )

    trip_category = MultipleChoiceFilter(
        field_name='trip_category',
        choices=Trip.TRIP_CATEGORY)
    trip_status = MultipleChoiceFilter(
        field_name='trip_status',
        choices=Trip.TRIP_STATUS)
    trip_shared = MultipleChoiceFilter(
        field_name='shared',
        choices=Trip.SHARE_CHOICES)
    start_date = DateFilter(
        field_name='start_date',
        lookup_expr='gte'
    )
    end_date = DateFilter(
        field_name='end_date',
        lookup_expr='lte'
    )

    def filter_current_user_trips(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(owner=user)
        return queryset

    def filter_liked_by_user(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(likes__owner=user)
        return queryset

    def filter_trip_by_profile(self, queryset, name, value):
        return queryset.filter(owner__profile=value)

    def filter_followed_users(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(owner__followed__owner=user)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data.get('owner__username') and 'request' in kwargs:
            self.data = self.data.copy()
            self.data['owner__username'] = kwargs['request'].user.username

    class Meta:
        model = Trip
        fields = [
            'start_date',
            'end_date',
            'owner__username',
            'place',
            'country',
            'trip_category',
            'trip_status',
            'liked_by_user',
        ]


class TripList(generics.ListCreateAPIView):
    """
    API view to retrieve list of trips or create a new trip.
    Attributes:
        serializer_class (TripSerializer): Serializer class used for the view.
        permission_classes (list): Permission classes for access to the view.
        queryset (QuerySet): The base queryset for retrieving trips,
                                annotated with likes and images count, and
                                ordered by creation date.
        filter_backends (list): List of filter backends used for filtering and
                                    searching the queryset.
        filterset_class (TripFilter): The filter class for the queryset.
        search_fields (list): List of fields that can be searched.
        ordering_fields (list): List of fields for ordering the queryset.
    Methods:
        perform_create(serializer):
            Saves the new trip instance with the owner set to the current user.
        get_serializer_context():
            Adds the current user to the serializer context.
    """

    serializer_class = TripSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Trip.objects.filter(
                Q(owner=user) | Q(shared=True)
                ).annotate(
                likes_count=Count('images__likes', distinct=True),
                images_count=Count('images', distinct=True),
            ).order_by('-created_at')

        return Trip.objects.filter(shared=True).annotate(
                likes_count=Count('images__likes', distinct=True),
                images_count=Count('images', distinct=True),
        ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_class = TripFilter

    search_fields = [
        'owner__username',
        'place',
        'country',
        'trip_category',
        'trip_status',
        'liked_by_user',
    ]
    ordering_fields = [
        'owner__username',
        'created_at',
        'updated_at',
        'likes_count',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TripDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a Trip instance.
    This view supports the following operations:
    - Retrieve a single Trip instance.
    - Update a Trip instance.
    - Delete a Trip instance.
    The queryset is annotated with:
    - likes_count: The count of likes associated with the images of the trip.
    - images_count: The count of images associated with the trip.
    The results are ordered by the creation date in descending order.
    Attributes:
        queryset (QuerySet): The base queryset for retrieving Trip instances.
        serializer_class (Serializer): The serializer class used for
            validating and deserializing input, and for serializing output.
        permission_classes (list): The list of permission classes that
            determine access control.
    """
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Trip.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ImageList(generics.ListCreateAPIView):
    """
    API view to retrieve a list of images or create a new image.
    Attributes:
        serializer_class (ImageSerializer): The serializer class for the view.
        permission_classes (list): Permission classes that the user must pass.
        filter_backends (list): List of filter backends used for ordering.
        ordering_fields (list): List of fields that can be used for ordering.
    Methods:
        get_queryset(self):
            Retrieves the queryset of images filtered by trip ID and owner.
        perform_create(self, serializer):
            Saves a new image instance with the current user as the owner and
                associates it with the specified trip.
    """

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['uploaded_at']

    def get_queryset(self):
        trip_id = self.kwargs.get('trip_id')
        trip = get_object_or_404(Trip, id=trip_id)
        user = self.request.user

        if user.is_authenticated:
            queryset = Image.objects.filter(
                 Q(trip=trip) & (Q(shared=True) | Q(trip__owner=user))
            )
        else:
            queryset = Image.objects.filter(trip=trip, shared=True)

        return queryset.distinct().order_by('-uploaded_at')

    def perform_create(self, serializer):
        trip = get_object_or_404(
            Trip,
            id=self.kwargs['trip_id'],
            owner=self.request.user
        )
        serializer.save(trip=trip)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete an Image instance.
    Allows users to perform the following actions on an Image instance:
    - Retrieve the details of an image.
    - Update the details of an image.
    - Delete an image.
    The view is restricted to the owner of the trip associated with the image.
    Attributes:
        serializer_class (ImageSerializer): Serializer class for the image.
        permission_classes (list): Permission classes for access to the view.
    Methods:
        get_queryset(self):
            Returns a queryset of Image objects filtered by the trip ID and
            the owner of the trip.
    """

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Image.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ImageListGallery(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['uploaded_at']
    queryset = Image.objects.all().filter(shared=True).order_by('-uploaded_at')


class ImageListGalleryDetail(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['uploaded_at']

    def get_queryset(self):
        image_id = self.kwargs['pk']
        return Image.objects.filter(pk=image_id)
