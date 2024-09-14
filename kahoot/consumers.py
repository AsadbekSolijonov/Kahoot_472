import json
from channels.generic.websocket import AsyncWebsocketConsumer


class KahootConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_pin = self.scope['url_route']['kwargs']['game_pin']
        self.room_group_name = f'kahoot_{self.game_pin}'

        # O'yinchi qo'shiladi
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # O'yinchi o'chiriladi
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Clientdan kelgan message (game-pin va username)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json['username']

        # Boshqa o'yinchilarga username yuboriladi
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_join',
                'username': username
            }
        )

    # O'yinchini o'yinga qo'shish
    async def player_join(self, event):
        username = event['username']

        # WebSocket orqali username ni front-endga yuborish
        await self.send(text_data=json.dumps({
            'message': f'{username} o\'yinga qo\'shildi!'
        }))
