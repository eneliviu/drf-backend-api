from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsOwnerOrReadOnly
from .models import Trip, Image
from .serializers import TripSerializer, ImageSerializer


# Create your views here.
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

    # `filterset_fields` for advanced filtering through complex
    # relationship pathways
    filterset_fields = [
        'owner__username',
        'country',
        'place',
        'trip_category',
        'trip_status',
        'start_date',
        'end_date',
    ]

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
