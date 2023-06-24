from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from apps.tkbot.models import openAI, BotPrompts,Bot
from apps.wsp.models import ChatWSP
from common.constants.constants import MSG_ROL
from apps.companies.models import Company
from .serializers import botPromptsSerializer
from apps.users.permissions import IsAdmin

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def checkIA(request):
  if request.method == 'POST':
    print('check ready')
    return Response({'status':'OK'}, status=status.HTTP_200_OK)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdmin])
def create_prompt_view(request):
  if request.method == 'POST':
    serializer = botPromptsSerializer(data=request.data,context={'user':request.user})
    if serializer.is_valid():
      serializer.save()
      return Response({'status':'OK'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdmin])
def edit_prompt_view(request):
  try: 
    instance = BotPrompts.objects.get(id=request.data['id'])
    serializer = botPromptsSerializer(instance=instance,data=request.data,context={'user':request.user},partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response({'status':'OK'}, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  except BotPrompts.DoesNotExist:
    return Response({'prompt_id': 'El prompt no exite'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdmin])
def delete_prompt_view(request, pk):
  try:
    botprompt = BotPrompts.objects.get(id=pk)
    botprompt.delete()
    return Response({'status': 'Deleted'}, status=status.HTTP_302_FOUND)
  except BotPrompts.DoesNotExist:
    return Response({'prompt_id': 'El prompt no exite'},status=status.HTTP_400_BAD_REQUEST)
