from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import OperatorRegistrationSerializer,OperatorUpdateSerializer,OperatorIdValidatorSerializer
from rest_framework import status
from apps.operators.models import Operator


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_operator_view(request):
  if request.method == 'POST':
    serializer = OperatorRegistrationSerializer(data=request.data,context=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_operator_view(request):
  if request.method == 'POST':
    validate_serializer = OperatorIdValidatorSerializer(data=request.data,context=request.data)
    if validate_serializer.is_valid():
      instance = Operator.objects.get(id = validate_serializer.validated_data['id'])
      update_serializer = OperatorUpdateSerializer(instance=instance , data=request.data,partial=True)
      if update_serializer.is_valid():
        update_serializer.save()
        return Response(update_serializer.data, status=status.HTTP_201_CREATED)
      return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(validate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # try:
      
      
      
    #   instance = Operator.objects.get(id=request.data['id'])
    # except:
    #   context_error={
    #     "id": "id del operador no se encontro"
    #   }
    #   return Response(context_error, status=status.HTTP_400_BAD_REQUEST)
      
    # serializer = OperatorUpdateSerializer(instance=instance,data=request.data)
    # if serializer.is_valid():
    #   serializer.save()
    #   return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
