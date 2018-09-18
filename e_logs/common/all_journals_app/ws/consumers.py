import json
import asyncio

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from e_logs.common.all_journals_app.models import Cell, Shift


class JournalInfoConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        self.channel = f"user_{self.scope['user'].employee.id}"
        await self.channel_layer.group_add(
            self.channel,
            self.channel_name,
        )

        await self.accept()


    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            f"user_{self.scope['user'].employee.id}",
            self.channel_name,
        )

        await self.close()
        raise StopConsumer()


    async def websocket_receive(self, event):
        text = event.get('text', None)
        if text is not None:
            data = json.loads(text)
            cell = await self.get_or_create_cell(data['cell_location'])
            value = data['value']
            await self.update_cell(cell, value)

            if cell.journal.type == 'shift':
                await self.add_shift_resonsible(shift_id=int(data['cell_location']['group_id']))

            await self.channel_layer.group_send(
                self.channel,
                {
                    "type": "send_message",
                    "text": json.dumps(data)
                }
            )

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
