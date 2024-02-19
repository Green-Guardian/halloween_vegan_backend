import json
from channels.generic.websocket import AsyncWebsocketConsumer

import logging


class ChatConsumer(AsyncWebsocketConsumer):
    logger = logging.getLogger(__name__)

    async def connect(self):
        self.logger.debug('WebSocket connection established')
        await self.channel_layer.group_add(
            "hw_admin_chat",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        self.logger.debug(f'WebSocket disconnected [{close_code=}]')
        await self.channel_layer.group_discard(
            "hw_admin_chat",
            self.channel_name
        )

    async def receive(self, text_data):
        self.logger.debug(f'Received message: {text_data}')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            "hw_admin_chat",
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
