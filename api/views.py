from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@api_view()
@permission_classes([AllowAny])
def root_route(request):
    '''
    This is the root route of the API.
    It is public and does not require authentication
    '''
    return Response({
        'message': 'Welcome to my trip planning API!'
    })
