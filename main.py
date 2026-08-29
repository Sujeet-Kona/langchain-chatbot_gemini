from dotenv import load_dotenv
import os

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in .env. Add GOOGLE_API_KEY and restart the app.")

st.set_page_config(page_title="Sujith langChatbot", page_icon="")
st.title("Ask something to the Sujith's AI Chatbot")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

user_input = st.chat_input("Type your message...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.chat_history.append(HumanMessage(content=user_input))
    conversation = []
    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            conversation.append(("human", msg.content))
        elif isinstance(msg, AIMessage):
            conversation.append(("ai", msg.content))

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a helpful, funny, and friendly AI assistant.
            Keep responses short and conversational and memorize past conversations.
            """
        ),
        *conversation,
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({})

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.chat_history.append(AIMessage(content=response))
