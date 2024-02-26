import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        print(self.room_id)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message:str = text_data_json['text']
        # if message.lower() == ''
        print(message)
        self.send(text_data=json.dumps({
            'text': f"You sent a message : {message}"
        }))
