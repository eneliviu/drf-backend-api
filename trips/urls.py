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
        name='trip_detail'
    ),
    path(
        'trips/<int:trip_id>/images/',
        views.ImageList.as_view(),
        name='image_list'
    ),
    path(
        'trips/<int:trip_id>/images/<int:pk>/',
        views.ImageDetail.as_view(),
        name='image-detail'
    ),
    path(
        'images/',
        views.ImageList.as_view(),
        name='image-detail'
    ),
    path(
        'images/<int:pk>/',
        views.ImageDetail.as_view(),
        name='image-detail'
    ),
]
