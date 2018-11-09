from channels.generic.websocket import WebsocketConsumer
from .teamJang import *
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': '오늘의 야구 경기를 시작하겠습니다!!',
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):

        text_data_json = json.loads(u'{"message":"지금은 새벽 5시"}')
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message,

        }))