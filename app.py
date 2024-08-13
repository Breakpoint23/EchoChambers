import streamlit as st
from echochambers.Crawler.WebGen import WebGenerator
from echochambers.Crawler.Summaraizer import Summerizer


st.set_page_config(page_title="EchoChambers",page_icon="🔊",layout="wide")

ss=st.session_state
if "web" not in st.session_state:
    st.session_state.web=WebGenerator(3)
    st.session_state.sum=Summerizer()

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.chat_message("assistant"):
        docs=st.session_state.web.invoke(prompt)
        answer=st.session_state.sum.invoke(prompt,docs)
        st.markdown(answer)