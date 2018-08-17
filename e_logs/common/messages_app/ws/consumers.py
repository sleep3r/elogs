import json
import asyncio
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from cacheops import cached_view_as
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from e_logs.common.all_journals_app.models import Cell, Comment
from e_logs.common.messages_app.models import Message
from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import model_to_dict, logged

from ..models import Message
from e_logs.common.login_app.models import Employee

class MessageConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        #задаем общую группу для рассыылки сообщений
        await self.channel_layer.group_add(
            "messages", #идентефикатор группы (не обязательно абсолютно уникальный)
            self.channel_name, #дефолтное значение
        )
        #ответ об успешном подключении к сокету
        await self.accept()

        await self.send_json({
            "text": await self.get(),
        })

    @database_sync_to_async
    def get(self):
        res = DeepDict()
        res['messages'] = {}
        for m in self.scope['user'].employee.unread_messages():
            res['messages'][m.id] = model_to_dict(m)
        return res

    async def websocket_receive(self, event):
        text = event.get('text', None)
        if text is not None:
            data = json.loads(text)

            response = {
                "text": data["message"],
            }
            #отправляет данные в канал, метод отправки ("type") нужно указать свой
            await self.channel_layer.group_send(
                "messages",
                {
                    "type": "message.all",
                    "text": f"{self.scope['user'].employee.name} "
                            f"ввел неверное значение: {response['text']['text']}"
                },
            )
    #кастомный метод отправки сообщения по группе "messages"
    async def message_all(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            "messages",  # идентефикатор группы (не обязательно абсолютно уникальный)
            self.channel_name,  # дефолтное значение
        )

        await self.close()


#Пример кода на JS _________________________________________________________________________________
#
# var endpoint = 'ws://' + window.location.host + '/messages/';
###<script src="{% static 'vendors/reconnecting-websocket/reconnecting-websocket.js' %}"></script>##
# socket = new ReconnectingWebSocket(endpoint);
#
# socket.onmessage = function (event) {
#     console.log("message", event);
# 	alert(event.data);
# };
# socket.onopen = function (event) {
#     console.log("connected", event);
# };
# socket.onerror = function (event) {
#     console.log("error", event);
# };
# socket.onclose = function (event) {
#     console.log("closed", event);
# };
#
# socket.send(JSON.stringify({"message":"Asmet Omarov comes"}))
#___________________________________________________________________________________________________