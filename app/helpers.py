import io

# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import pickle
import random
import string

import requests
import ast
from django.core.files.uploadedfile import InMemoryUploadedFile

from firebase_admin import credentials, initialize_app, storage
import os
import datetime
import firebase_admin
import tempfile
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from SorayiaAPI import settings
from app.data import def_prompt, PROMPT


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def upload_file(file, folder, prevent_content_type=False):
    # print(file.name)
    # print(file.content_type)
    # json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'services.json')
    if not firebase_admin._apps:
        cred = credentials.Certificate("services.json")
        initialize_app(cred, {'storageBucket': 'sorayia-d28db.appspot.com'})
    # Client = storage.storage.Client.from_service_account_info(json_file_path)
    bucket = storage.bucket('sorayia-d28db.appspot.com')
    random_name = generate_random_string(10)
    extension = file.name.split('.')[1] if prevent_content_type is False else 'txt'
    libelle = f"{random_name}.{extension}"
    blob_name = os.path.join(folder, libelle)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        expiration=datetime.timedelta(minutes=20),
        method="PUT",
        version='v4',
        # content_type="application/octet-stream",
        content_type='text/plain' if prevent_content_type else file.content_type
    )
    print(url)
    file.seek(0)
    final_url = f"https://storage.googleapis.com/sorayia-d28db.appspot.com/{folder}/{libelle}"
    response = requests.put(url, headers={'Content-Type': 'text/plain' if prevent_content_type else file.content_type},
                            data=file.read())
    print(response)
    return {"public_url": final_url, "type": extension}


def make_split_doc(files):
    documents = []
    for file in files:
        if file.type == 'pdf':
            loader = PyPDFLoader(file.url)
            documents.extend(loader.load_and_split())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits: list = text_splitter.split_documents(documents)
    # print(splits)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
        tmp.write(pickle.dumps(splits))
        response = upload_file(tmp, "split_docs", True)
    return response


def load_list_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        content = response.content
        print('gobe')
        # print(type(pickle.loads(content)))
        # Assuming the content of the file is a valid Python list literal
        data_list = pickle.loads(content)
        # print(data_list)
        return data_list
    except requests.exceptions.RequestException as e:
        print(f"Error loading data from URL: {e}")
        return None


def generated_code():
    return str(random.randint(100000, 999999))


def get_desc_prompt(type, name) -> str:
    if type == '1':
        prompt = PROMPT[0]
        return def_prompt(name, prompt.get('titre'), prompt.get('objectif'), prompt.get('caracteristique'))

    if type == '2':
        prompt = PROMPT[1]
        return def_prompt(name, prompt.get('titre'), prompt.get('objectif'), prompt.get('caracteristique'))

    if type == '3':
        prompt = PROMPT[2]
        return def_prompt(name, prompt.get('titre'), prompt.get('objectif'), prompt.get('caracteristique'))

    return "Data Not Found"


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# def gpt_with_content_based():
#     qa_system_prompt = """Tu est un assistant utile. Sers toi des informations ci-dessous pour répondre aux question.
#     {context}
#
#     Voilà la quetion de l'utilistateur :
#     """
#     qa_prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", qa_system_prompt),
#             MessagesPlaceholder(variable_name="chat_history"),
#             ("human", "{question}"),
#         ]
#     )

def send_gpt(context, model, human_prompt, human_input, previous_messages, splits=None):
    # rag_prompt_template = """
    # Tu est un assistant utile. Sers toi des informations ci-dessous pour répondre aux question.
    # {context}
    #
    # Voilà la quetion de l'utilistateur : {user_input}
    #
    # """
    retriever = None
    # print(splits)
    # rag_prompt = PromptTemplate.from_template(rag_prompt_template)
    # print(type(splits))
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    # splits = None
    vectorstore = None
    # print(splits)
    if splits is not None:
        # splits = list()
        vectorstore = Chroma.from_documents(documents=splits,
                                            embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))

        # Retrieve and generate using the relevant snippets of the blog.
        retriever = vectorstore.as_retriever()

    chat = ChatOpenAI(model_name=model, temperature=0.7, openai_api_key=OPENAI_API_KEY, )
    print(context)
    system_message_prompt = SystemMessagePromptTemplate.from_template(context)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt)
    message_placeholder = MessagesPlaceholder(variable_name="chat_history")

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, message_placeholder, human_message_prompt]
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chat_history_buffer = []
    for msg in previous_messages:
        if msg["type"] == "user":
            chat_history_buffer.append(HumanMessage(content=msg["message"]))
            memory.chat_memory.add_user_message(msg["message"])
        else:
            chat_history_buffer.append(AIMessage(content=msg["message"]))
            memory.chat_memory.add_ai_message(msg["message"])

    # rag_chain = (
    #         {"context": retriever | format_docs, "user_input": RunnablePassthrough()}
    #         # {"context": retriever | format_docs, "question": ""}
    #         | chat_prompt
    #         | chat
    #         | StrOutputParser()
    # )
    if retriever is None:
        chain = LLMChain(llm=chat, prompt=chat_prompt, memory=memory, verbose=True)
    else:
        # chain = (
        #         {"context": retriever | format_docs, "user_input": RunnablePassthrough()}
        #         # {"context": retriever | format_docs, "question": ""}
        #         | chat_prompt
        #         | chat
        #         | StrOutputParser()
        # )

        contextualize_q_chain = chat_prompt | chat | StrOutputParser()

        def contextualized_question(input: dict):
            if input.get("chat_history"):
                return contextualize_q_chain
            else:
                return input["question"]

        rag_chain = (
                RunnablePassthrough.assign(
                    context=contextualized_question | retriever | format_docs
                )
                | chat_prompt
                | chat
        )

        response = rag_chain.invoke({"question": human_input, "chat_history": chat_history_buffer})
        print(response.content)
        vectorstore.delete_collection()
        return response.content
    response = chain.run(human_input)
    print(response)
    return response
