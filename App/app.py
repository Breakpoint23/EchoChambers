import streamlit as st
from echochambers.Chain.customChain import CustomChain


st.set_page_config(page_title="Streamlit App", page_icon=":shark:", layout="wide")

ss=st.session_state

if "chain" not in ss:
    ss.chain=CustomChain()
    ss.history=[]
    ss.messages=[]


for message in ss.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask me anything"):

    ss.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        answer=ss.chain.invoke(prompt)
        st.markdown(answer)
        ss.messages.append({"role":"assistant","content":answer})



