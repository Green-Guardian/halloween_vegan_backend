import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from app.chat.models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    logger = logging.getLogger(__name__)

    async def connect(self):
        self.logger.debug('WebSocket connection established')
        await self.channel_layer.group_add(
            "hw_admin_chat",
            self.channel_name
        )
        await self.accept()

        messages = await self.get_chat_messages()
        for message, username in messages:
            await self.send(text_data=json.dumps({
                'message': message,
                'user': username
            }))

    @database_sync_to_async
    def get_chat_messages(self):
        messages = ChatMessage.objects.all().order_by('-created_at')[:20]
        messages_list = [(message.message, message.user.username) for message in messages]
        messages_list.reverse()
        return messages_list

    async def disconnect(self, close_code):
        self.logger.debug(f'WebSocket disconnected [{close_code=}]')
        await self.channel_layer.group_discard(
            "hw_admin_chat",
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.create_chat_message(user=self.scope['user'], message=message)

        await self.channel_layer.group_send(
            "hw_admin_chat",
            {
                'type': 'chat_message',
                'message': message
            }
        )

    @database_sync_to_async
    def create_chat_message(self, user, message):
        return ChatMessage.objects.create(user=user, message=message)

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
