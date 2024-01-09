import random
from firebase_admin import credentials, initialize_app, storage

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def upload_file(file):
    cred = credentials.Certificate("templates/services.json")
    initialize_app(cred, {'storageBucket': 'sorayia-d28db.appspot.com'})

    bucket = storage.bucket()
    blob = bucket.blob(file.name)
    blob.upload_from_filename(file.read())
    blob.make_public()
    return blob.public_url


def delete_file_remote(filename):
    if filename is not None:
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.delete()


def generated_code():
    return str(random.randint(100000, 999999))


def send_gpt(context, model, human_prompt, human_input, previous_messages):
    chat = ChatOpenAI(model_name=model, temperature=0.7, max_tokens=500)

    system_message_prompt = SystemMessagePromptTemplate.from_template(context)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt)
    message_placeholder = MessagesPlaceholder(variable_name="chat_history")

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, message_placeholder, human_message_prompt]
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    for msg in previous_messages:
        if msg["type"] == "user":
            memory.chat_memory.add_user_message(msg["message"])
        else:
            memory.chat_memory.add_ai_message(msg["message"])

    chain = LLMChain(llm=chat, prompt=chat_prompt, memory=memory, verbose=True)
    response = chain.run(human_input)
    return response

