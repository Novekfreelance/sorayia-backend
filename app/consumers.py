import json
from channels.generic.websocket import WebsocketConsumer

from app import models, helpers


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        print(self.room_id)
        self.bot = models.Bot.objects.get(pk=self.room_id)
        self.chat = models.Chat.objects.create(bot=self.bot)
        # self.chat = self.chat
        # print(self.chat)
        self.accept()

        if "Relation Client" in self.bot.prompt:
            self.send(text_data=json.dumps({
                'text': f"Quel est votre nom et prénom ?",
                'state': 0
            }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message: str = text_data_json['text']
        if text_data_json.get('state') == 0:
            self.send(text_data=json.dumps({
                'text': f"Quel est votre email ?: {message}",
                'state': 1
            }))
        elif text_data_json.get('state') == 1:
            self.send(text_data=json.dumps({
                'text': f"Merci. En quoi puis-je vous aider?",
                'state': None
            }))
        else:
            previous_messages = []
            previous_object = models.Message.objects.filter(chat__id=self.chat.id)
            for message_ in previous_object:
                previous_messages.append({'type': message_.model, 'message': message_.content})

            bot = models.Bot.objects.get(pk=self.room_id)
            files_list = []
            for folder in bot.folders.all():
                # folder = models.Folder.objects.prefetch_related('file_set').get(pk=folder_id)
                files_list.extend(folder.file_set.all())
            response_splits = helpers.load_list_from_url(bot.split_url)

            gpt_response = helpers.send_gpt(
                context=bot.description if bot.prompt is None or bot.prompt == 'Date not found' else bot.prompt,
                model=bot.model,
                human_prompt='{question}',
                human_input=message,
                previous_messages=previous_messages,
                splits=response_splits
            )

            gpt_message = models.Message.objects.create(
                chat_id=self.chat.id,
                bot_id=bot.pk,
                model='system',
                type='text',
                content=gpt_response,
                user_id=None
            )

            gpt_message.save()
            self.chat.messages.add(gpt_message)

            # if message.lower() == ''
            print(message)
            self.send(text_data=json.dumps({
                'text': f"{gpt_response}"
            }))
