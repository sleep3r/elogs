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
        try:
            self.data_channel = 'data'
            self.user_channel = f"user_{self.scope['user'].employee.id}"

            await self.channel_layer.group_add(
                self.user_channel,
                self.channel_name,
            )

            await self.channel_layer.group_add(
                self.data_channel,
                self.channel_name,
            )

            await self.accept()

        except:
            await self.close()

    async def websocket_disconnect(self, event):
        try:
            await self.channel_layer.group_discard(
                self.user_channel,
                self.channel_name,
            )

            await self.channel_layer.group_discard(
                self.data_channel,
                self.channel_name,
            )
        except:
            pass

        await self.close()
        raise StopConsumer()

    async def websocket_receive(self, event):
        text = event.get('text', None)
        if text is not None:
            data = json.loads(text)
            print(data)
            if data['type'] == 'shift_data':
                await self.shift_receive(data)

            elif data['type'] == 'messages':
                await self.messages_receive(data)

            elif data['type'] == 'make_responsible':
                await self.add_shift_resonsible(shift_id=int(data['group_id']))

    async def send_message(self, event):
        await self.send(event['text'])

    async def shift_receive(self, data):

        for cell_data in data['cells']:
            employee = self.scope['user'].employee
            cell_data['responsible'] = {str(employee.user):employee.name}

        await self.channel_layer.group_send(
            self.data_channel,
            {
                "type": "send_message",
                "text": json.dumps(data)
            }
        )

        for cell_data in data['cells']:
            cell = await self.get_or_create_cell(cell_data['cell_location'])
            value = cell_data['value']
            await self.update_cell(cell, value)

            if cell.journal.type == 'shift':
                await self.add_shift_resonsible(shift_id=int(cell_data['cell_location']['group_id']))


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
        cell.responsible = self.scope['user'].employee
        cell.value = value
        cell.save()

    @database_sync_to_async
    def add_shift_resonsible(self, shift_id):
        shift = Shift.objects.get(id=shift_id)
        shift.responsibles.add(self.scope['user'].employee)

    # ----------------------------------MESSAGES----------------------------------
    async def add_cell_message(self, data):
        if data['message']['type'] == "critical_value":
            cell = await self.get_cell_from_dict(data['cell'])
            if cell:
                message = data['message'].copy()
                message['sendee'] = self.scope['user'].employee
                await self.add_cell_message_query(message, cell, all_users=True)

        elif data['message']['type'] == "comment":
            message = data['message'].copy()
            message['sendee'] = self.scope['user'].employee
            text = message['text']

            cell = await self.get_or_create_cell(data['cell_location'])

            if cell:
                comment = await self.add_comment_query(cell, text)

                data['created'] = comment.created.isoformat()
                data['employee'] = {str(comment.employee.user):comment.employee.name}
                await self.channel_layer.group_send(
                    self.data_channel,
                    {
                        "type": "send_message",
                        "text": json.dumps(data)
                    }
                )
                await self.add_cell_message_query(message, cell, all_users=True)

    @database_sync_to_async
    def get_or_create_cell(self, cell_location):
        return Cell.get_or_create_cell(**cell_location)

    @database_sync_to_async
    def add_comment_query(self, cell, text):
        comment = Comment.objects.create(
            content_type=ContentType.objects.get_for_model(cell),
            object_id=cell.id,
            text=text,
            employee=self.scope['user'].employee)

        return comment

    @database_sync_to_async
    def get_cell_from_dict(self, cell_dict: dict) -> Cell:
        field_name = cell_dict['field_name']
        table_name = cell_dict['table_name']
        group_id = cell_dict['group_id']
        index = cell_dict['index']

        return Cell.get_by_addr(field_name, table_name, group_id, index)

    @database_sync_to_async
    def add_cell_message_query(self, message, cell, all_users=False, positions=None, uids=None,
                               plant=None):
        Message.add(message, cell, all_users, positions, uids, plant)

    @database_sync_to_async
    def update(self, cell):
        Message.update(cell)
