from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from . models import Group, Chat
from channels.db import database_sync_to_async
class MyWebsocketConsumer(WebsocketConsumer):
    
    def connect(self):
        print('Websocket connected')
        print("channel layer", self.channel_layer)
        print("channel name", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        print('Group name', self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        self.accept()
    
    def receive(self, text_data=None, bytes_data=None):
        print('Websocket message received', text_data)
        data = json.loads(text_data)
        message = data['msg']
        group = Group.objects.get(name = self.group_name)
        chat = Chat(
            content = data['msg'],
            group = group
        )
        chat.save()
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'chat.message',
                'message': message
            }
        )
    
    def chat_message(self,event):
        print("Event", event)
        self.send(text_data= json.dumps({
            'msg': event['message']
        }))
        
    def disconnect(self, code=None):
        print('Websocket closed', code)
        print('Channel layer', self.channel_layer)
        print('Channel channel name', self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )
        

class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print("channel layer", self.channel_layer)
        print("channel name", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        print('Group name', self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()
        
    async def receive(self, text_data=None, bytes_data=None):
        print('Websocket message received', text_data)
        data = json.loads(text_data)
        message = data['msg']
        group = await database_sync_to_async(Group.objects.get)(name = self.group_name)
        chat = Chat(
            content = data['msg'],
            group = group
        )
        await database_sync_to_async(chat.save)()
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'chat.message',
                'message': message
            }
        )
    async def chat_message(self,event):
        print("Event", event)
        await self.send(text_data= json.dumps({
            'msg': event['message']
        }))
        
           
    async def disconnect(self, code=None):
        print('Websocket closed', code)
        print('Channel layer', self.channel_layer)
        print('Channel channel name', self.channel_name)
        self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )