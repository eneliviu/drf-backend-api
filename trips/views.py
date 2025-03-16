from django.shortcuts import get_object_or_404
from django.db.models import Count, Q  # Subquery, OuterRef, Sum
# from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import (
    FilterSet, DateFilter, CharFilter, MultipleChoiceFilter,
    BooleanFilter,
)
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from api.permissions import IsOwnerOrReadOnly
from .models import Trip, Image
from .serializers import TripSerializer, ImageSerializer


class UserFilteredMixin:
    """
    A mixin that provides filtering methods for queryset based on
    the authenticated user.
    Methods
    -------
    filter_liked_by_user(queryset, name, value)
        Filters the queryset to include only the objects liked by the
        authenticated user if the value is True.
    filter_followed_users(queryset, name, value)
        Filters the queryset to include only the objects owned by users
        followed by the authenticated user if the value is True.
    """
    def filter_liked_by_user(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(likes__owner=user)
        return queryset

    def filter_followed_users(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(owner__followed__owner=user)
        return queryset


class TripFilter(UserFilteredMixin, FilterSet):
    """
    A filter class for filtering Trip instances based on various criteria.
    Attributes:
        owner__username (CharFilter): Filters trips by the owner's username.
        country (CharFilter): Filters trips by country.
        place (CharFilter): Filters trips by place.
        liked_by_user (BooleanFilter): Filters trips liked by the current user.
        user_trips (BooleanFilter): Filters trips by the user's profile.
        current_user_trips (BooleanFilter): Filter trips owned by current user.
        followed_users (BooleanFilter): Filters trips by followed users.
        trip_category (MultipleChoiceFilter): Filters trips by category.
        trip_status (MultipleChoiceFilter): Filters trips by status.
        trip_shared (BooleanFilter): Filters trips by shared status.
        start_date (DateFilter): Filters trips starting from a specific date.
        end_date (DateFilter): Filters trips ending by a specific date.
    Methods:
        filter_current_user_trips(queryset, name, value):
            Filters trips to include only those owned by the
                current user if authenticated.
    Meta:
        model (Trip): The model to filter.
        fields (list): The list of fields that can be filtered.
    """

    owner__username = CharFilter(field_name='owner__username')
    country = CharFilter(field_name='country')
    place = CharFilter(field_name='place')
    trip_shared = BooleanFilter(field_name='shared')
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')

    profile_id = CharFilter(field_name='owner__profile__id')

    liked_by_user = BooleanFilter(
        method='filter_liked_by_user',
        field_name='liked'
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
        choices=Trip.TRIP_CATEGORY
    )

    trip_status = MultipleChoiceFilter(
        field_name='trip_status',
        choices=Trip.TRIP_STATUS
    )

    def filter_current_user_trips(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(owner=user)
        return queryset

    class Meta:
        model = Trip
        fields = [
            'start_date', 'end_date', 'owner__username', 'place', 'country',
            'trip_category', 'trip_status', 'liked_by_user', 'trip_shared',
            'start_date', 'end_date',
            'profile_id'
        ]


class ImageFilter(UserFilteredMixin, FilterSet):
    """
    A filter class for filtering Image objects based on various fields.
    Attributes (case-insensitive):
        owner__username (CharFilter): Filters images by the owner's username
        image_title (CharFilter): Filters images by their title.
        description (CharFilter): Filters images by their description.
        shared (BooleanFilter): Filters images by their shared status.
        uploaded_at (DateFilter): Filters images by their upload date range.
        followed_users (BooleanFilter): Filters images by followed users.
        liked_by_user (BooleanFilter): Filters images liked by the user.
    Methods:
        filter_image_title(queryset, name, value): Filter by image title.
        filter_description(queryset, name, value): Filter by description.
        filter_shared(queryset, name, value): Filter by shared status.
        filter_uploaded_at(queryset, name, value): Filter by upload date range.
    """
    owner__username = CharFilter(
        field_name='owner__username',
        lookup_expr='iexact'
    )
    image_title = CharFilter(
        field_name='image_title',
        method='filter_image_title',
        lookup_expr='icontains'
    )
    description = CharFilter(
        field_name='description',
        method='filter_description',
        lookup_expr='icontains'
    )
    shared = BooleanFilter(
        field_name='shared',
        method='filter_shared'
    )
    uploaded_at = DateFilter(
        field_name='uploaded_at',
        lookup_expr='range',
        method='filter_uploaded_at'
    )

    followed_users = BooleanFilter(
        method='filter_followed_users',  # Inherited from the mixin
        field_name='followed_users'
    )

    liked_by_user = BooleanFilter(
        method='filter_liked_by_user',
        field_name='liked_by_user'
    )

    like_id = BooleanFilter(
        method='filter_like_id',
        field_name='like_id'
    )

    def filter_image_title(self, queryset, name, value):
        if value:
            return queryset.filter(image_title__icontains=value)
        return queryset

    def filter_description(self, queryset, name, value):
        if value:
            return queryset.filter(description__icontains=value)
        return queryset

    def filter_shared(self, queryset, name, value):
        return queryset.filter(shared=value)

    def filter_uploaded_at(self, queryset, name, value):
        if value:
            return queryset.filter(uploaded_at__range=value)
        return queryset

    def filter_like_id(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(likes__owner=user)
        return queryset

    class Meta:
        model = Image
        fields = [
            'owner__username', 'image_title', 'description', 'shared',
            'uploaded_at', 'like_id', 'liked_by_user'
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
        filterset_class (CustomFilter): The filter class for the queryset.
        search_fields (list): List of fields that can be searched.
        ordering_fields (list): List of fields for ordering the queryset.
    Methods:
        perform_create(serializer):
            Saves the new trip instance with the owner set to the current user.
        get_serializer_context():
            Adds the current user to the serializer context.
    """

    serializer_class = TripSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        '''
        Returns a queryset of Trip objects with additional annotations and filters.
        The queryset is annotated with:
            - images_count: The count of associated images, distinct by trip.
            - total_likes_count: The total count of likes for all images
                associated with the trip, ensuring each like is counted only once.
        The queryset is ordered by the creation date of the trips in descending order.
        If the user is authenticated, the queryset includes trips that are shared.
        If the user is not authenticated, the queryset includes only shared trips.
        '''
        user = self.request.user
        if user.is_authenticated:
            queryset = Trip.objects.filter(
                Q(shared=True) | Q(owner=user)
            ).annotate(
                images_count=Count('images', distinct=True),
                total_likes_count=Count('images__likes', distinct=True),
            ).order_by('-created_at')
        else:
            queryset = Trip.objects.filter(shared=True).annotate(
                images_count=Count('images', distinct=True),
                total_likes_count=Count('images__likes', distinct=True),
            ).order_by('-created_at')

        return queryset

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
        'start_date',
        'end_date'
    ]
    ordering_fields = [
        'owner__username',
        'created_at',
        'updated_at',
        'likes_count',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TripListPublic(generics.ListCreateAPIView):
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
        filterset_class (CustomFilter): The filter class for the queryset.
        search_fields (list): List of fields that can be searched.
        ordering_fields (list): List of fields for ordering the queryset.
    Methods:
        perform_create(serializer):
            Saves the new trip instance with the owner set to the current user.
        get_serializer_context():
            Adds the current user to the serializer context.
    """

    serializer_class = TripSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Returns a queryset of Trip objects with additional annotations
        and filters. The queryset is annotated with:
            - images_count: The count of associated images, distinct by trip.
            - total_likes_count: The total count of likes for all images
                associated with the trip.
        The queryset is ordered by the creation date of the trips
            in descending order.
        If the user is authenticated, the queryset includes trips that are
            either shared or owned by the user.
        If the user is not authenticated, the queryset includes only
            shared trips.
        Returns:
            QuerySet: A queryset of Trip objects with the applied annotations
                and filters.
        """
        queryset = Trip.objects.annotate(
            images_count=Count('images', distinct=True),
            total_likes_count=Count('images__likes', distinct=True)
        )
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(Q(shared=True) | Q(owner=user))
        else:
            queryset = queryset.filter(shared=True)

        return queryset.order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_class = TripFilter

    search_fields = [
        'owner__username',
        'trip_place',
        'trip_country',
        'trip_category',
        'trip_status',
        'start_date',
        'end_date'
    ]
    ordering_fields = [
        'owner__username',
        'created_at',
        'updated_at',
        'likes_count',
    ]

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
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
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    filterset_class = ImageFilter
    ordering_fields = ['uploaded_at', 'likes_count', 'owner__username']
    search_fields = [
        'owner__username',
        'image_title',
        'description'
    ]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    def get_queryset(self):
        trip_id = self.kwargs.get('trip_id')
        trip = get_object_or_404(Trip, id=trip_id)
        user = self.request.user

        if user.is_authenticated:
            queryset = Image.objects.filter(
                 Q(trip=trip) & (Q(shared=True) | Q(trip__owner=user))
            ).annotate(
                likes_count=Count('likes')
            )
        else:
            queryset = Image.objects.filter(
                trip=trip,
                shared=True
            ).annotate(
                likes_count=Count('likes')
            )

        return queryset.distinct().order_by('-uploaded_at')

    def perform_create(self, serializer):
        trip = get_object_or_404(
            Trip,
            id=self.kwargs['trip_id']
        )
        if trip.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to upload images for this trip."
                )
        serializer.save(
            trip=trip,
            owner=self.request.user
        )

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST
            )

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
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Image.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ImageListGallery(generics.ListCreateAPIView):
    """
    API view to retrieve and create images in the gallery.
    This view supports listing and creating images. It uses the
    `ImageSerializer` for serialization and applies the
    `IsAuthenticatedOrReadOnly` permission class, allowing authenticated
    users to create images while others can only read.
    Attributes:
        serializer_class (ImageSerializer): Serializer class used for the view.
        permission_classes (list): Permission classes applied to the view.
        filter_backends (list): Filter backends for filtering and ordering.
        filterset_class (ImageFilter): ilter class for filtering the queryset.
        ordering_fields (list): Fields for ordering the results.
        search_fields (list): List of fields that can be searched.
    Methods:
        get_queryset(): Returns the queryset of shared images, annotated with
                        the count of likes, and ordered by the upload date in
                        descending order.
    """

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]

    filterset_class = ImageFilter

    ordering_fields = ['uploaded_at', 'likes_count', 'owner__username']

    search_fields = [
        'owner__username',
        'image_title',
        'description',
        'shared',
        'uploaded_at',
        'trip__trip_category',
        'trip__trip_status',
        'trip__shared'
    ]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    def get_queryset(self):
        return Image.objects.filter(shared=True)\
            .annotate(likes_count=Count('likes'))\
            .order_by('-uploaded_at')


class ImageListGalleryDetail(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['uploaded_at']

    def get_queryset(self):
        image_id = self.kwargs['pk']
        return Image.objects.filter(pk=image_id)
