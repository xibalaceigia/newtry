import os
from chromadb.api.types import Document
from langchain_chroma import Chroma
from utils.config_handler import chroma_conf
from model.factory import embed_model, chat_model
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader,text_loader,listdir_with_allowed_type,get_file_md5_hex
from utils.loger_handler import logger



class VectorStoreService:
    def __init__(self, ):
        self.vector_store = Chroma(
            collection_name = chroma_conf["collection_name"],
            embedding_function = embed_model,
            persist_directory = chroma_conf["persist_directory"],
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_conf["chunk_size"],
            chunk_overlap = chroma_conf["chunk_overlap"],
            separators = chroma_conf["separators"],
            length_function = len,
        )

    def get_retriver(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})



    def load_document(self)->None:
        """
        从数据文件夹读取数据文件，转为向量存入向量库
        要计算md5值并去重
        """
        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(chroma_conf["md5_hex_store"]):
                open(chroma_conf["md5_hex_store"], "w", encoding="utf-8").close()
                return False#没处理过

            with open(chroma_conf["md5_hex_store"], "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if line.strip() == md5_for_check:
                        return True#已处理过
                return False#没处理过
            
        def save_md5_hex(md5_for_save:str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_save + "\n")

        def get_file_document(read_path:str)->Document:
            if read_path.endswith("txt"):
                return text_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []
            
        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allowed_file_types"]),
        )
            
        for path in allowed_files_path:
            #获取文件的md5
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"文件{path}已处理过，跳过")
                continue
            try:#这里没错，是list[Document]，因为text_loader / pdf_loader 本身返回的就是列表
                documents: list[Document] = get_file_document(path)

                if not documents:
                    logger.warning(f"文件{path}没有有效内容，跳过")
                    continue
                split_document: list[Document] = self.splitter.split_documents(documents)
                
                if not split_document:
                    logger.warning(f"文件{path}分片后没有有效内容，跳过")
                    continue
                #将内容存入向量库
                self.vector_store.add_documents(split_document)
                save_md5_hex(md5_hex)
                logger.info(f"文件{path}加载成功，处理完成")
            except Exception as e:
                #exc_info = True记录详细报错堆栈，False仅记录报错信息本身
                logger.error(f"文件{path}处理失败: {str(e)}, exc_info = True")
                continue



if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_document()
    retriver = vs.get_retriver()
    res = retriver.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("="*20)
