import json
import asyncio
import urllib.parse

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.contenttypes.models import ContentType

from e_logs.common.all_journals_app.models import Cell, Shift, Comment
from e_logs.common.messages_app.models import Message


class CommonConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        query = dict(urllib.parse.parse_qsl(self.scope['query_string'].decode("utf-8")))
        shift_id = query.get('shift', None)
        self.user_channel = f"user_{self.scope['user'].employee.id}"
        if shift_id:
            self.shift_channel = f"shift_{shift_id}"
            await self.channel_layer.group_add(
                self.shift_channel,
                self.channel_name,
            )

        await self.channel_layer.group_add(
            "messages",
            self.channel_name,
        )

        await self.channel_layer.group_add(
            self.user_channel,
            self.channel_name,
        )

        await self.accept()

    async def websocket_disconnect(self, event):
        if hasattr(CommonConsumer, 'shift_channel'):
            await self.channel_layer.group_discard(
                self.shift_channel,
                self.channel_name,
            )

        await self.channel_layer.group_discard(
            "messages",
            self.channel_name,
        )

        await self.channel_layer.group_discard(
            self.user_channel,
            self.channel_name,
        )
        await self.close()
        raise StopConsumer()

    async def websocket_receive(self, event):
        text = event.get('text', None)
        if text is not None:
            data = json.loads(text)
            if data['type'] == 'shift_data':
                await self.shift_receive(data)

            elif data['type'] == 'messages':
                if data['crud'] == 'add':
                    await self.add_cell_message(data)

                elif data['crud'] == 'update':
                    cell = await self.get_cell_from_dict(data['cell'])
                    if cell:
                        await self.update(cell)

    async def shift_receive(self, data):
        cell = await self.get_or_create_cell(data['cell_location'])
        value = data['value']
        await self.update_cell(cell, value)

        if cell.journal.type == 'shift':
            await self.add_shift_resonsible(shift_id=int(data['cell_location']['group_id']))

        await self.channel_layer.group_send(
            self.shift_channel,
            {
                "type": "send_message",
                "text": json.dumps(data)
            }
        )

    async def messages_receive(self, data):
        if data['crud'] == 'add':
            await self.add_cell_message(data)

        elif data['crud'] == 'update':
            cell = await self.get_cell_from_dict(data['cell'])
            if cell:
                await self.update(cell)

    @database_sync_to_async
    def get_or_create_cell(self, cell_location):
        return Cell.get_or_create_cell(**cell_location)

    @database_sync_to_async
    def update_cell(self, cell, value):
        if value != '':
            cell.responsible = self.scope['user'].employee
            cell.value = value
            cell.save()
        else:
            cell.delete()

    @database_sync_to_async
    def add_shift_resonsible(self, shift_id):
        shift = Shift.objects.get(id=shift_id)
        shift.employee_set.add(self.scope['user'].employee)

    async def send_message(self, event):
        await self.send(event['text'])

    #----------------------------------MESSAGES----------------------------------
    async def add_cell_message(self, data):
        if data['message']['type'] == "critical_value":
            cell = await self.get_cell_from_dict(data['cell'])
            if cell:
                message = data['message'].copy()
                message['sendee'] = self.scope['user'].employee
                await self.add_cell_message_query(cell, message, all_users=True)

        elif data['message']['type'] == "comment":
            message = data['message'].copy()
            message['sendee'] = self.scope['user'].employee
            text = message['text']

            cell = await self.get_or_create_cell(data['cell_location'])

            if cell:
                await self.add_comment_query(cell, text)
                await self.add_cell_message_query(cell, message, all_users=True)

    @database_sync_to_async
    def get_or_create_cell(self, cell_location):
        return Cell.get_or_create_cell(**cell_location)

    @database_sync_to_async
    def add_comment_query(self, cell, text):
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
    def add_cell_message_query(self, cell, message, all_users=False, positions=None, uids=None, plant=None):
         Message.add(cell, message, all_users, positions, uids, plant)

    @database_sync_to_async
    def update(self, cell):
        Message.update(cell)