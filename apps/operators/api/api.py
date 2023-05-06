from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import OperatorRegistrationSerializer
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_operato_view(request):
  if request.method == 'POST':
    print(request.data)
    serializer = OperatorRegistrationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
