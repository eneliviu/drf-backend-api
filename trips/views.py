from django.db.models import Count
from django_filters import FilterSet, DateFilter, CharFilter, CharFilter, MultipleChoiceFilter
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsOwnerOrReadOnly
from .models import Trip, Image
from .serializers import TripSerializer, ImageSerializer
from datetime import datetime


class TripFilter(FilterSet):
    """
    TripFilter is a filter set for filtering Trip objects based on various fields.
    Attributes:
        owner__username (CharFilter): Filters trips by the username of the owner.
        country (CharFilter): Filters trips by the country.
        place (CharFilter): Filters trips by the place.
        trip_category (CharFilter): Filters trips by the trip category.
        trip_status (CharFilter): Filters trips by the trip status.
        start_date (DateFilter): Filters trips that start on or after a given date.
        end_date (DateFilter): Filters trips that end on or before a given date.
    Meta:
        model (Model): The model that this filter set is based on.
        fields (list): The list of fields that can be filtered.
    """

    owner__username = CharFilter(field_name='owner__username')
    country = CharFilter(field_name='country')
    place = CharFilter(field_name='place')
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     if not self.data.get('start_date'):
    #         self.data = self.data.copy()
    #         self.data['start_date'] = datetime.now().date().strftime('%Y-%m-%d')
    #     if not self.data.get('end_date'):
    #         self.data = self.data.copy()
    #         self.data['end_date'] = datetime.now().date().strftime('%Y-%m-%d')
        if not self.data.get('owner__username') and 'request' in kwargs:
            self.data = self.data.copy()
            self.data['owner__username'] = kwargs['request'].user.username

    class Meta:
        model = Trip
        fields = ['start_date', 'end_date']


class TripList(generics.ListCreateAPIView):
    '''
    List all trips or create a new trip.
    '''
    serializer_class = TripSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Trip.objects.annotate(
            # comments_count=Count('comment', distinct=True),
            # likes_count=Count('likes', distinct=True),
            images_count=Count('images', distinct=True)
        ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_class = TripFilter
    # filterset_fields = [
    #     'owner__username',
    #     'country',
    #     'place',
    #     'trip_category',
    #     'trip_status',
    #     'start_date',
    #     'end_date',
    # ]

    ordering_fields = [
        'owner__username',
        'created_at',
        'updated_at',
        # 'liked_by_user',
        # 'user_posts',
        # 'current_user_posts',
        # 'followed_users'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class TripDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a Trip instance.
    Attributes:
        queryset (QuerySet): The base queryset for retrieving Trip instances.
        serializer_class (Serializer): Serializer class for Trip instances.
        permission_classes (list): Dermission classes for access control.
    Methods:
        get_queryset(): Annotates queryset with the count of related images.
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Trip.objects.annotate(
            images_count=Count('images')
        )


class ImageList(generics.ListCreateAPIView):
    '''
    List all images or create a new image.
    '''
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['uploaded_at']

    def get_queryset(self):
        queryset = Image.objects.order_by('-uploaded_at')
        owner_username = self.request.query_params.get('owner__username', None)
        if owner_username:
            queryset = queryset.filter(owner__username=owner_username)
        return queryset


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete an image instance.
    '''
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        trip_id = self.kwargs['trip_id']
        return Image.objects.filter(trip__id=trip_id)
