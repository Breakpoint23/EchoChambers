import os
import uuid
import time

from langchain_groq import ChatGroq
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_chroma import Chroma
from langchain_text_splitters import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.retrievers.multi_vector import SearchType

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.storage import InMemoryByteStore

from langchain_core.retrievers import BaseRetriever

# Testing

from echochambers.Crawler.WebGen import WebGenerator

os.environ["GROQ_API_KEY"] = "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"
#os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "sk-proj-jkccOV7WIPxjwqBpKex7T3BlbkFJj3UOc7dXM8UcxjZdnZhi"


class MultiVecRetriever():

    def __init__(self) -> None:


        #self.llm=ChatGroq(temperature=0.2,model="llama3-70b-8192")
        self.llm=ChatOpenAI(temperature=0.2)
        self.parentSplitter=TokenTextSplitter(chunk_size=2000,chunk_overlap=150)
        self.childSplitter=TokenTextSplitter(chunk_size=1000,chunk_overlap=50)
        self.embeddings=OpenAIEmbeddings()
        self.vectorDB=Chroma(collection_name="summaries",embedding_function=self.embeddings)
        self.store=InMemoryByteStore()
        self.idKey="doc_id"

        self.retriever=self.getRetriever()
        self.retriever.search_type=SearchType.mmr
    

    
    def addDocuments(self,docDict,question:str):

        docs=[]
        for i in range(3):
            docs+=self.parentSplitter.create_documents(texts=[docDict["content"][i]],metadatas=[{"source":docDict["source"][i]}])

        self.documents=docs
        
        inDocs=[]
        for doc in self.documents:
            inDocs.append({"doc":doc,"question":question})

        sumChain=self.getSumChain()

        prev_time=time.time()
        try:
            summaries=sumChain.batch(inDocs,{"max_concurrency":3})
        except Exception as e:
            print("Error in summarization: ",e)
            summaries=[]
            for inputs in inDocs:
                summaries.append(sumChain.invoke(inputs))

        print("Time taken for summarization: ",time.time()-prev_time)

        doc_ids=[str(uuid.uuid4()) for _ in self.documents]

        summary_docs=[Document(page_content=s,metadata={self.idKey:doc_ids[i]}) for i,s in enumerate(summaries)]
        self.retriever.vectorstore.add_documents(summary_docs)
        self.retriever.docstore.mset(list(zip(doc_ids,self.documents)))
        
        

        return None
    
    def getSumChain(self):

        chain=({"doc": lambda x:x["doc"].page_content,"question": lambda x:x["question"]} | ChatPromptTemplate.from_template("Summarize the document keeping the user question in mind:\n question : {question}\ndoc: {doc}") | self.llm | StrOutputParser())

        return chain

    def getRetriever(self):

        return MultiVectorRetriever(vectorstore=self.vectorDB,byte_store=self.store,id_key=self.idKey)
    
    def invoke(self,question:str):
            
        return self.retriever.invoke(question)

    def _get_relevant_documents(self,question:str):
        return self.invoke(question)

if __name__ == "__main__":
    webGen=WebGenerator(3)
    retriever=MultiVecRetriever()

    docDict=webGen.invoke("I'm having a CSRF token cookie issue with django. How do I fix it?")
    
    retriever.addDocuments(docDict,"How do I fix a CSRF token cookie issue with django?")

    docs=retriever.invoke("How do I fix a CSRF token cookie issue with django?")

    with open("output.md","w") as f:
        for doc in docs:
            f.write(doc.page_content+"\n\n")