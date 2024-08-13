import os
import time
import tqdm

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from echochambers.Crawler.WebGen import WebGenerator
from echochambers.Chain.customRetriever import MultiVecRetriever


class CustomChain():

    def __init__(self):

        self.llm=ChatOpenAI(temperature=0.2)
        self.retriever=MultiVecRetriever()
        self.webGen=WebGenerator(3)
        self.generatePrompt()
        self.chain=self.makeChain()
        self.initFlag=True
        


    def initInvoke(self,question:str):

        docDict=self.webGen.invoke(question)
        self.retriever.addDocuments(docDict,question)
        self.initFlag=False
        return None
    

    def invoke(self,question:str):
            
        if self.initFlag:
            self.initInvoke(question)
        
        answer=self.chain.invoke({"input":question},config={"configurable":{"session_id":"test"}})["answer"]

        return answer



    def makeChain(self):

        history_aware_retriever=create_history_aware_retriever(self.llm,self.retriever.retriever,self.contextualize_q_prompt)
        question_answer_chain=create_stuff_documents_chain(self.llm,self.qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        self.store={}
        conversational_rag_chain = RunnableWithMessageHistory(
                                rag_chain,
                                self.get_session_history,
                                input_messages_key="input",
                                history_messages_key="chat_history",
                                output_messages_key="answer",
                            )

        return conversational_rag_chain


    def get_session_history(self,session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def generatePrompt(self):

        contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
        )


        self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        systemPrompt= """
        You are an assistant helping a user with their questions.
        Use the following pieces of retrieved context to answer 
        the question. If you don't know the answer, say that you don't know.

        context: {context}
        """
        self.qa_prompt=ChatPromptTemplate.from_messages(
            [
                ("system",systemPrompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}")
            ]
        )

        return None
    
