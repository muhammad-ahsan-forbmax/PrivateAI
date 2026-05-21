import threading

from langchain_openai import ChatOpenAI
from django_eventstream import send_event

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from chat.models import Message


def start_stream_thread(chat):
    thread = threading.Thread(target=stream_chat_response, kwargs={"chat": chat}, daemon=True)
    thread.start()


def stream_chat_response(chat):
    channel = f"chat-{chat.id}"

    try:
        messages = Message.objects.filter(chat=chat).order_by("-time")[:5]
        messages = reversed(messages)

        langchain_messages = [SystemMessage(content=("You are a helpful AI assistant."))]

        for message in messages:
            if not message.text:
                continue

            if message.role == Message.RoleChoice.USER:
                langchain_messages.append(HumanMessage(content=message.text))

            elif message.role == Message.RoleChoice.ASSISTANT:
                langchain_messages.append(AIMessage(content=message.text))

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, streaming=True)

        full_response = ""

        for chunk in llm.stream(langchain_messages):
            token = chunk.content

            if not token:
                continue

            full_response += token

            send_event(channel, "token", {"token": token})

        Message.objects.create(chat=chat, role=Message.RoleChoice.ASSISTANT, text=full_response)
        send_event(channel, "done", {"message": "completed"})

    except Exception as e:
        send_event(channel, "error", {"error": str(e)})
