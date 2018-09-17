import json
import asyncio

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DataConsumer(AsyncJsonWebsocketConsumer):
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

            await self.channel_layer.group_send(
                self.channel,
                {
                    "type": "send_message",
                    "text": json.dumps(data)
                }
            )


    async def message_send(self, event):
        await self.send({
            "type":"websocket.send",
            "text": event['text']
        })