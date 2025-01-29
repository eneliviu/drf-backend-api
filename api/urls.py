from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)
from .views import root_route

# from profiles.views import CustomAuthToken
from profiles.views import CustomTokenObtainPairView

urlpatterns = [
    path('', root_route),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # path(
    #     'api-auth/token/',
    #     TokenObtainPairView.as_view(),
    #     name='token_obtain_pair'
    # ),

    # path('api-auth/token/', CustomAuthToken.as_view(), name='custom_token_obtain_pair'),
    path('api-auth/token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),

    path(
        'api-auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/',
        include('dj_rest_auth.registration.urls')
    ),

    path('', include('profiles.urls')),
    path('', include('trips.urls')),
    path('', include('likes.urls')),
    path('', include('followers.urls')),

    path(
        'schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
