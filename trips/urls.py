from django.urls import path
from . import views as views

urlpatterns = [
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
        'images/',
        views.ImageListGallery.as_view(),
        name='image-gallery'
    ),
    path(
        'images/<int:pk>/',
        views.ImageListGalleryDetail.as_view(),
        name='detail-gallery'
    ),
]
