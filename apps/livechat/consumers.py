import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    await self.accept()
    await self.channel_layer.group_add('chat',self.channel_name)
    # channel_layer = get_channel_layer()
    await self.channel_layer.group_send(
        'chat',
        {
            'type': 'user_connected',
            'message': 'Un nuevo usuario se ha conectado'
        }
    )

  async def disconnect(self, close_code):
        await self.channel_layer.group_discard('chat', self.channel_name)

  async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']

    await self.channel_layer.group_send(
      'chat',
      {
        'type': 'chat_message',
        'message': message
      }
    )
    
  async def chat_message(self, event):
    message = event['message']
    await self.send(text_data=json.dumps({
        'message': message
    }))
    
  async def user_connected(self, event):
    message = event['message']
    await self.send(text_data=json.dumps({
        'message': message
    }))