import os
from googlesearch import search
import requests
import tiktoken
import time


from langchain.docstore.document import Document
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain_text_splitters import TokenTextSplitter

from langchain.chains.llm import LLMChain
from langchain_groq import ChatGroq



os.environ["GROQ_API_KEY"] = "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"



obj=search("Indian Goverment on Pulwama Attack", num_results=5)



class WebGenerator():

    """
    The reason for class implementation is that, known websites will have custom rules
    for scrapping and only forwarding useful information
    
    """

    def __init__(self,searchNum=5):

        self.JINA="r.jina.ai/"
        self.num=searchNum
        self.tokenizer=tiktoken.get_encoding("cl100k_base")


    
    def invoke(self,question: str) -> dict:

        output={"source":[],"content":[],"tokens":[]}

        gen=search(question,num_results=self.num)

        for url in gen:
            jinaUrl=self.makeUrl(url)
            try:

                response=requests.get(jinaUrl)
                prev_time=time.time()
                print(f"Got response: {url}")
                tokens=self.getTokens(response.text)
                print(f"Tokenization done in : {time.time()-prev_time}")
                
                output["source"].append(url) 
                output["tokens"].append(tokens)
                output["content"].append(response.text)
            except Exception as e:
                print(e,jinaUrl)


        return output
    
    def makeUrl(self,url):

        splitUrl=url.split("//")

        if len(splitUrl)==2:

            return splitUrl[0]+"//"+self.JINA+splitUrl[1]
    
        else:
            
            print("#"*100,"\n",f"found multiple splits{splitUrl}")
            return splitUrl[0]+"//"+self.JINA+"//".join(splitUrl[1:])


    def splitDocs(self,question):
        docDict=self.invoke(question)
        
        docs=[]
        for i in range(self.num):
            docs.append(Document(page_content=docDict["content"][i],metadata={"source":docDict["source"][i]}))

        return None


    def getTokens(self,text:str):

        tokens=self.tokenizer.encode(text)

        return tokens        



if __name__=="__main__":

    instance=WebGenerator()
    j=0
    while True:
        question=input("Ask a question:")
        output=instance.invoke(question)
        text=""
        for i in range(5):
            print(len(output["tokens"][i]))
            text+=output["content"][i]

        with open(f"output{j}.md","w") as f:
            f.write(text)

        j+=1










