"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""

from rag.vector_store import VectorStoreService
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
from utils.prompt_loader import load_rag_prompt
from chromadb.api.types import Document



class RagSummaryService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriver()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()


    def _init_chain(self):
        return self.prompt_template | self.model | StrOutputParser()

    def retriver_docs(self,query:str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query:str) -> str:  #用户提问交给检索器，检索完chroma返回参考资料，之后把参考资料给模型，返回模型的回答。
        #这个回答是一个基于问题的参考资料的总结，最终目的也是为了给下一次输入准备参考资料总结
        context_docs = self.retriver_docs(query)    #这是检索器拿到的参考资料

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】：参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"
  
        return self.chain.invoke(
            {
                "input": query,
                "context": context
            }
        )



if __name__ == "__main__":
    rag_summary_service = RagSummaryService()
    print(rag_summary_service.rag_summarize("小户型适合哪种扫地机器人"))


