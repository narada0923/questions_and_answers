from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings

class StoreService:
    def get_vectorstore_from_url(self, url: str) -> Chroma:
        loader = WebBaseLoader(url)
        document = loader.load()

        text_splitter = RecursiveCharacterTextSplitter()
        document_chunks = text_splitter.split_documents(document)

        vectorestore = Chroma.from_documents(document_chunks, OpenAIEmbeddings(chunk_size=1))

        return vectorestore
    
    def get_vectorstore_from_document(self, chunks: list[str]):
        embeddings = OpenAIEmbeddings(chunk_size=1)
        vectorstore = Chroma.from_texts(texts=chunks, embedding=embeddings)
        return vectorstore

store_service = StoreService()