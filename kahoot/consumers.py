# consumers.py
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Game, Player


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_pin = self.scope['url_route']['kwargs']['pin_code']
        self.game_group_name = f'game_{self.game_pin}'

        # Join the game group
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the game group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    # Receive messages from WebSocket (client)
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']

        if action == 'join':
            nickname = data['nickname']
            game = await self.get_game(self.game_pin)
            if not await self.player_exists(nickname, game):
                player = await self.create_player(nickname, game)

                # Broadcast the updated player list
                await self.channel_layer.group_send(
                    self.game_group_name,
                    {
                        'type': 'player_update',
                        'action': 'join',
                        'nickname': nickname,
                        'player_id': player.id,
                    }
                )

        elif action == 'remove':
            player_id = data['player_id']
            await self.remove_player(player_id)

            # Broadcast player removal to the group
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'player_update',
                    'action': 'remove',
                    'player_id': player_id,
                }
            )

        elif action == 'start_game':
            game = await self.get_game(self.game_pin)
            game.started = True
            game.is_active = False
            await self.save_game(game)

            # Broadcast game start to the group
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'game_start',
                }
            )

    # Send updates to WebSocket clients (broadcasting)
    async def player_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def game_start(self, event):
        await self.send(text_data=json.dumps({
            'action': 'start_game'
        }))

    # Database operations
    @sync_to_async
    def get_game(self, pin_code):
        return Game.objects.get(pin_code=pin_code)

    @sync_to_async
    def player_exists(self, nickname, game):
        return Player.objects.filter(nickname=nickname, game=game).exists()

    @sync_to_async
    def create_player(self, nickname, game):
        return Player.objects.create(nickname=nickname, game=game)

    @sync_to_async
    def remove_player(self, player_id):
        Player.objects.filter(id=player_id).delete()

    @sync_to_async
    def save_game(self, game):
        game.save()
