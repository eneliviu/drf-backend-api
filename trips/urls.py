from django.urls import path
from . import views as views

urlpatterns = [
    path(
        'public/',
        views.TripListPublic.as_view(),
        name='trip_list_public'
    ),
    path(
        'trips/',
        views.TripList.as_view(),
        name='trip_list'
    ),
    path(
        'trips/<int:pk>/',
        views.TripDetail.as_view(),
        name='trip-detail'
    ),
    path(
        'trips/<int:trip_id>/images/',
        views.ImageList.as_view(),
        name='image-list-trip'
    ),
    path(
        'trips/<int:trip_id>/images/<int:pk>/',
        views.ImageDetail.as_view(),
        name='image-detail'
    ),
    path(
        'gallery/',
        views.ImageListGallery.as_view(),
        name='image-gallery'
    ),
    path(
        'gallery/<int:pk>/',
        views.ImageListGalleryDetail.as_view(),
        name='detail-gallery'
    ),
]
