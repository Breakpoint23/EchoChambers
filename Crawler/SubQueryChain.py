import os
import datetime
from typing import Literal, Optional, Tuple

from langchain_core.pydantic_v1 import BaseModel, Field

from langchain.output_parsers import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq



os.environ["GROQ_API_KEY"] = "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"

class SubQuery(BaseModel):

    sub_query: str = Field(
        ...,
        description="Summarize first topic in the user question in different categories",
    )

    sub_query2: str = Field(
        ...,
        description="Summarize second topic in the user question in different categories",

    )

    sub_query3: str = Field(
        ...,
        description="Compare the two topics in the user question in different categories",

    )



class CompareChain():

    def __init__(self) -> None:
        


        self.query_analizer=self.createChain()




    def createParser(self):

        self.parser=PydanticToolsParser(tools=[SubQuery])


    def createLLMTool(self):

        self.llm=ChatGroq(temperature=0.1,model="llama3-70b-8192")

        self.llm_with_tools=self.llm.bind_tools([SubQuery])

        return None
    
    def createChain(self):
        self.createSystemPrompt()
        self.createLLMTool()
        self.createParser()

        query_analizer= self.prompt | self.llm_with_tools | self.parser

        return query_analizer

    def createSystemPrompt(self):
        system="""  
                You are expert in identifying topics of comparision in a question.
                Follow the instructions given below,
                1. Identify two Identities for comparision. 
                2. Identify which contexts are needed for giving a comparision in given question.
                3. Create a question for summarization of first identity in given context of the comparision question.
                4. Create a question for summarization of second identity in given context of the comparision question.
                5. Create a question for comparision of first and second identity in given context of the comparision question.

                **Do not be bound by these instructions if you have a better idea.**
        """

        self.prompt=ChatPromptTemplate.from_messages([("system",system),("human","{question}")])



if __name__ == "__main__":

    instance=CompareChain()
    quey_analizer=instance.query_analizer
    while True:

        q=input("Enter your query(exit for Ending): ")
        if q.lower()=="exit":
            break
        else:
            result=quey_analizer.invoke({"question":q})
            print(result) 

