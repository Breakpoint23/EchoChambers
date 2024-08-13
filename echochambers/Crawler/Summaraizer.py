import os
import tiktoken
import time
from tqdm import tqdm

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from langchain_text_splitters import TokenTextSplitter
from langchain.docstore.document import Document

from echochambers.Crawler.WebGen import WebGenerator




os.environ["GROQ_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "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"
class Summerizer():

    def __init__(self):
        self.encoder=tiktoken.get_encoding("cl100k_base")
        self.splitter=TokenTextSplitter(chunk_size=4000,chunk_overlap=500)

        self.llm=ChatOpenAI(temperature=0.2)
        self.documents={}
        self.chain=self.getChain()
        self.invokeChain=self.getInvokeChain()
        self.chunkChain=self.getChunkSumChain()
        


    def newAddDocument(self,text:str,source:str,question:str):

        doc=Document(page_content=text,page_metadata={"source":source})
        doc=self.splitter.split_documents([doc])

        if len(doc)==1:
            summaries=self.chunkChain.invoke({"question":question,"doc":doc})

        else:
            sums=[]
            args={"question":question}
            for i in range(len(doc)):
                partSum=self.chunkChain.invoke({"question":question,"doc":doc[i]})
                sums.append(partSum)
                args["summary"+str(i+1)]=partSum

            sumChain=self.getSumChain(len(doc))
            summaries=sumChain.invoke(args)

        return summaries

    def getChain(self):

        sumPrompt=self.getPrompt()
        parser=StrOutputParser()

        chain= sumPrompt | self.llm | parser


        return chain

    def getPrompt(self):

        SummaraizationPrompt=ChatPromptTemplate.from_template(""" Given the user question,

        a previous summary of the document , and current chunk of the document,create a new document that is
        more concise and
        that contains all the information required to answer the
        user query that is contained in the document.

        user question: {question}
        Previous Summary: {summary1}
        New document: {doc}

        ** You do not need to be much concise, Your priotiy is to encode all the information
        related to user question and hence can be a verbose summary**
        """)

        return SummaraizationPrompt

    def getInvokePropt(self):
        invokePrompt=ChatPromptTemplate.from_template("""
        Given the user question, and summaries from the documents that might contain the answer,
        provide the answer to the user question in a verbose manner.
        question: {question}
        summary : {summary}
        answer it in a markdown format.
        """)
        return invokePrompt
    
    def getConciseSumPrompt(self):
        prompt=ChatPromptTemplate.from_template("""
        Given the user question, and a chunk from the documents that might contain the answer,
        create a concise summary that contains all the relevant information regarding user question.
        question: {question}
        doc : {doc}
        """)
        return prompt

    def getAllSumPrompt(self,numChunks:int):
        promptText="""
        given the user question, and summaries from the document chunks create a new document that is
        more concise and that contains all the information required to answer the user query that is contained in the document.
        Question: {question}
        """
        for i in range(numChunks):
            promptText+="Summary: {summary"+str(i+1)+"}\n"
        prompt=ChatPromptTemplate.from_template(promptText)
        return prompt

    def getChunkSumChain(self):
        prompt=self.getConciseSumPrompt()
        parser=StrOutputParser()
        chain=prompt | self.llm | parser
        return chain
    
    def getSumChain(self,numChunks:int):
        prompt=self.getAllSumPrompt(numChunks)
        parser=StrOutputParser()
        chain=prompt | self.llm | parser
        return chain

    def getInvokeChain(self):
        invokePrompt=self.getInvokePropt()
        parser=StrOutputParser()
        chain=invokePrompt | self.llm | parser

        return chain

    def updatedInvoke(self,question:str,docs:dict):
        output={"source":[],"summary":[],"numTokens":[]}
        totalTokens=0
        for i in tqdm(range(len(docs["source"])),total=len(docs["source"])):
            output["source"].append(docs["source"][i])
            summary=self.newAddDocument(docs["content"][i],docs["source"][i],question)
            numTokens=len(self.encoder.encode(summary))
            totalTokens+=numTokens
            output["summary"].append(summary)
            output["numTokens"].append(numTokens)
            
        splitSummary=self.splitSummary(output,totalTokens)
        print(len(splitSummary))
        if len(splitSummary)==1:
            answer=self.invokeChain.invoke({"question":question,"summary":splitSummary[0]})
            print(splitSummary[0])
        else:
            args={"question":question}
            for i in range(len(splitSummary)):
                args["summary"+str(i+1)]=splitSummary[i]

            sumChain=self.getSumChain(len(splitSummary))
            summary=sumChain.invoke(args)
            answer=self.invokeChain.invoke({"question":question,"summary":summary})
        
            print(summary)
        return answer

    
    def splitSummary(self,output:dict,totalTokens:int):
        totalSummary=""
        for i in range(len(output["summary"])):
            totalSummary+="Source URL:"+ output["source"][i] + "\n"
            totalSummary+=output["summary"][i] + "\n"

        if totalTokens>5500:
            print(f"Total tokens are greater than 5500 : {totalTokens}, Splitting the summary.")
            splitSummary=self.splitter.split_text(totalSummary)
        else:
            splitSummary=[totalSummary]

        return splitSummary








if __name__=="__main__":

    instance=Summerizer()
    webgen=WebGenerator(3)
    docs=webgen.invoke("""
            Forbidden (403)

            CSRF verification failed. Request aborted.
            I'm getting this error when I try to interact with a django app
            """)
    question="How to resolve this CSRF Verication failed error in the Django app?"
    output=instance.updatedInvoke(question,docs)


    with open("sumOutput.md","w") as f:
        f.write(output)
