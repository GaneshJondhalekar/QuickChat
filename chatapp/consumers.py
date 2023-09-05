# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import SyncConsumer
import json
from .models import ChatMessage
from django.contrib.auth.models import User
import threading
import asyncio
import json
from channels.db import database_sync_to_async
class ChatConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def save_message(self, sender, receiver, message):
         ChatMessage.objects.create(
                    sender=sender,
                    receiver=receiver,
                    message=message,
                )   
    async def connect(self):
        self.user_id = int(self.scope['user'].id)
        #print(self.scope['url_route']['kwargs']['username'],'hiiiii')
        self.other_user_id = self.scope['url_route']['kwargs']['username']
        #self.room_name ='b'
        self.other_user_ids=list(map(int,self.other_user_id.split('_')))
        self.other_user_ids.remove(self.user_id)
        print(self.other_user_ids,self.user_id)
        ids=sorted([self.user_id,self.other_user_ids[0]])
        self.room_name = f'{ids[0]}_{ids[1]}'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        #print('reciever...',self.other_user_id)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender=self.scope['user']
        receiver=await database_sync_to_async(User.objects.get)(pk=self.other_user_ids[0])
        #print('recivedMsg :',message)
        await self.save_message(sender, receiver, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'sender_id': self.scope['user'].id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event.get('sender_id', None)  # Get the sender_id from the event if available
        
        # Exclude the original sender when sending the message back
        if sender_id != self.scope['user'].id:
            print('Received message from user', sender_id)
            print('Received message:', message)
            
            await self.send(text_data=json.dumps({
                'message': message,
                'sender_id': sender_id  # Include sender_id in the message data
            }))
       
            
    