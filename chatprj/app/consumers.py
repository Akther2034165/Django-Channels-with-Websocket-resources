from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from . models import Group, Chat
from channels.db  import database_sync_to_async
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Websocket connected...', event)
        print("Channel Layer...", self.channel_layer)
        print("Channel Name...", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
            )
        self.send({
            'type': 'websocket.accept'
        })
        
    # def websocket_receive(self, event):
    #     print('Received from Client...', event['text'])
    #     data = json.loads(event['text'])
    #     print(data)
    #     print('user............................', self.scope['user'])
    #     #find group
    #     group = Group.objects.get(name = self.group_name)
    #     # create chat object
    #     if self.scope['user'].is_authenticated:
    #         chat = Chat(
    #             content = data['msg'],
    #             group = group
    #         )
    #         chat.save()
    #         async_to_sync(self.channel_layer.group_send)(
    #             self.group_name, 
    #             {
    #                 'type' : 'chat.message',
    #                 'message' : event['text']
    #             }
    #         )
    #     else:
    #         self.send({
    #             'type' : 'websocket.send',
    #             'text' : json.dumps({"msg":"Login Requeired"})
    #         })
            
    # def chat_message(self, event):
    #     print('Event', event)
    #     print('Actual Data', event['message'])
    #     self.send({
    #         'type' : 'websocket.send',
    #         'text' : event['message']
    #     })
    
    def websocket_receive(self, event):
        print('Received from Client...', event['text'])
        data = json.loads(event['text'])
        print(data)
        print('user............................', self.scope['user'])
        #find group
        group = Group.objects.get(name = self.group_name)
        # create chat object
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = data['msg'],
                group = group
            )
            chat.save()
            data['user'] = self.scope['user'].username
            print('Complete Data', data)
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, 
                {
                    'type' : 'chat.message',
                    'message' : json.dumps(data)
                }
            )
        else:
            self.send({
                'type' : 'websocket.send',
                'text' : json.dumps({"msg":"Login Requeired", "user":"guest"})
            })
            
    def chat_message(self, event):
        print('Event', event)
        print('Actual Data', event['message'])
        self.send({
            'type' : 'websocket.send',
            'text' : event['message']
        })
        
    
    def websocket_disconnect(self, event):
        print('Websocket disconnected...', event)
        print("Channel Layer...", self.channel_layer)
        print("Channel Name...", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
            )
        raise StopConsumer()
    

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Websocket connected...', event)
        print("Channel Layer...", self.channel_layer)
        print("Channel Name...", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        await self.channel_layer.group_add(
            self.group_name , self.channel_name
            )
        await self.send({
            'type': 'websocket.accept'
        })
        
    # async def websocket_receive(self, event):
    #     print('Received from Client...', event['text'])
    #     data = json.loads(event['text'])
    #      #find group
    #     group = Group.objects.get(name = self.group_name)
    #     # create chat object
    #     if self.scope['user'].is_authenticated:
    #         chat = Chat(
    #             content = data['msg'],
    #             group = group
    #         )
    #         await database_sync_to_async(chat.save)()
    #         await self.send({
    #             'type' : 'websocket.send',
    #             'text' : event['msg']
    #         })
        
    #         await self.channel_layer.group_send(
    #             self.group_name , 
    #             {
    #                 'type' : 'chat.message',
    #                 'message' : event['text']
    #             }
    #         )
    #     else:
    #         await self.send({
    #             'type' : 'websocket.send',
    #             'text' : json.dumps({"msg":"Login Requeired", "user":"guest"})
    #         })
    
    async def websocket_receive(self, event):
        print('Received from Client...', event['text'])
        data = json.loads(event['text'])
         #find group
        group = Group.objects.get(name = self.group_name)
        # create chat object
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = data['msg'],
                group = group
            )
            await database_sync_to_async(chat.save)()
            data['user'] = self.scope['user'].username
            await self.send({
                'type' : 'websocket.send',
                'text' : json.dumps(data)
            })
        
            await self.channel_layer.group_send(
                self.group_name , 
                {
                    'type' : 'chat.message',
                    'text' : json.dumps(data)
                }
            )
        else:
            await self.send({
                'type' : 'websocket.send',
                'text' : json.dumps({"msg":"Login Requeired", "user":"guest"})
            })
            
    async def chat_message(self, event):
        print('Event', event)
        print('Actual Data', event['message'])
        
    async def websocket_disconnect(self, event):
        print('Websocket disconnected...', event)
        print("Channel Layer...", self.channel_layer)
        print("Channel Name...", self.channel_name)
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
            )
        raise StopConsumer()