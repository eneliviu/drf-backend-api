from django.urls import path
from . import views as views

urlpatterns = [
    path(  # List of all shared trips
        'trips/',
        views.TripList.as_view(),
        name='trip_list'
    ),
    path(  # Detail view of a shared trip
        'trips/<int:pk>/',
        views.TripDetail.as_view(),
        name='trip-detail'
    ),
    path(  # List of all shared images in a trip detail
        'trips/<int:trip_id>/images/',
        views.ImageList.as_view(),
        name='image-list-trip'
    ),
    path(  # Detaile view of a shared image in a trip detail
        'trips/<int:trip_id>/images/<int:pk>/',
        views.ImageDetail.as_view(),
        name='image-detail'
    ),
    path(  # List of all shared images
        'gallery/',
        views.ImageListGallery.as_view(),
        name='image-gallery'
    ),
    path( # Detaile view of a shared image
        'gallery/<int:pk>/',
        views.ImageListGalleryDetail.as_view(),
        name='detail-gallery'
    ),
]
