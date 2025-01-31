import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message, ChatRoom
from biwah.models import UserDatabase
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_username = text_data_json['sender_username']

        # Fetch chat room and sender asynchronously
        chat_room = await self.get_chat_room(self.room_name)
        sender = await self.get_sender(sender_username)

        # Save message to the database
        await self.save_message(chat_room, sender, message)

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_username': sender_username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_username = event['sender_username']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_username': sender_username
        }))

    # Async database functions
    @database_sync_to_async
    def get_chat_room(self, room_name):
        return ChatRoom.objects.get(room_name=room_name)

    @database_sync_to_async
    def get_sender(self, username):
        return UserDatabase.objects.get(username=username)

    @database_sync_to_async
    def save_message(self, chat_room, sender, content):
        Message.objects.create(chat_room=chat_room, sender=sender, content=content)
