import json
import asyncio
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from cacheops import cached_view_as
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from e_logs.common.all_journals_app.models import Cell, Comment
from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.loggers import err_logger

from ..models import Message
from e_logs.common.login_app.models import Employee

class MessageConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        #задаем общую группу для рассыылки сообщений
        await self.channel_layer.group_add(
            "messages", #идентефикатор группы (не обязательно абсолютно уникальный)
            self.channel_name, #дефолтное значение
        )
        await self.channel_layer.group_add(
            f"user_{self.scope['user'].employee.id}",  # идентефикатор группы (не обязательно абсолютно уникальный)
            self.channel_name,  # дефолтное значение
        )
        #ответ об успешном подключении к сокету
        await self.accept()

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            "messages",  # идентефикатор группы (не обязательно абсолютно уникальный)
            self.channel_name,  # дефолтное значение
        )
        await self.channel_layer.group_discard(
            f"user_{self.scope['user'].employee.id}",  # идентефикатор группы (не обязательно абсолютно уникальный)
            self.channel_name,  # дефолтное значение
        )

        await self.close()

    async def websocket_receive(self, event):
        text = event.get('text', None)
        if text is not None:
            data = json.loads(text)
            if data['crud'] == 'add':
                if data['message']['type'] == "critical_value":
                    cell = await self.get_cell_from_dict(data['cell'])
                    if cell:
                        message = data['message'].copy()
                        message['sendee'] = self.scope['user'].employee
                        await self.add(cell, message, all_users=True)

                elif data['message']['type'] == "comment":
                    message = data['message'].copy()
                    message['sendee'] = self.scope['user'].employee
                    text = message['text']

                    cell = await self.get_or_create_cell(data['cell_location'])

                    if cell:
                        await self.add_comment(cell, text)
                        await self.add(cell, message, all_users=True)

            elif data['crud'] == 'update':
                cell = await self.get_cell_from_dict(data['cell'])
                if cell:
                    await self.update(cell)

    #кастомный метод отправки сообщения по группе "messages"
    async def message_send(self, event):
        await self.send(event['text'])

    @database_sync_to_async
    def get_or_create_cell(self, cell_location):
        return Cell.get_or_create_cell(**cell_location)

    @database_sync_to_async
    def add_comment(self, cell, text):
        Comment.objects.update_or_create(
            content_type=ContentType.objects.get_for_model(cell),
            object_id=cell.id,
            defaults={'text': text,
                      'employee': self.scope['user'].employee})

    @database_sync_to_async
    def get_cell_from_dict(self, cell_dict: dict) -> Cell:
        field_name = cell_dict['field_name']
        table_name = cell_dict['table_name']
        group_id = cell_dict['group_id']
        index = cell_dict['index']

        return Cell.get_by_addr(field_name, table_name, group_id, index)

    @database_sync_to_async
    def add(self, cell, message, all_users=False, positions=None, uids=None, plant=None):
         Message.add(cell, message, all_users, positions, uids, plant)

    @database_sync_to_async
    def update(self, cell):
        Message.update(cell)
