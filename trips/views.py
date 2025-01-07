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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
        # 'owner__follows__followed_by__profile',
        # 'owner__followed_by__owner__profile',
        # trips_count,
        # 'images_count'
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
    '''
    Retrieve, update or delete a trip instance.
    '''
    queryset = Trip.objects.first()
    serializer_class = TripSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        # Annotate the queryset with the image count
        return Trip.objects.annotate(
            images_count=Count('images')
        )


class ImageList(generics.ListCreateAPIView):
    '''
    List all images or create a new image.
    '''
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerOrReadOnly]  # [IsAuthenticated]
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
    serializer_class = ImageSerializer
    queryset = Image.objects.first()
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        trip_id = self.kwargs['trip_id']
        return Image.objects.filter(trip__id=trip_id)


class TripImageUploadView(generics.CreateAPIView):
    '''
    Upload an image to a trip.
    '''
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(pk=trip_id)
        serializer.save(owner=self.request.user, trip=trip)