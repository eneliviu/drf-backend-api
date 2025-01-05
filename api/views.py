from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view()
@permission_classes([AllowAny])
def root_route(request):
    return Response({
        'message': 'Welcome to my api!'
    })
