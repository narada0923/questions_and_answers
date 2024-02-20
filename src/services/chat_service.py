from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import streamlit as st

class ChatService:
    def get_context_retriever_chain(self, vectorstore: Chroma):
        llm = ChatOpenAI()
        retriever = vectorstore.as_retriever()

        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            ("user", "Given the above conversation, generate a search query to look up in order to get information revelant to the conversation.")
        ])

        retriever_chain = create_history_aware_retriever(llm=llm, retriever=retriever, prompt=prompt)
        return retriever_chain
    

    def get_conversational_rag_chain(self, retriever_chain):
        llm = ChatOpenAI()

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer the user's question based on the context:\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ])

        stuff_document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

        return create_retrieval_chain(retriever_chain, stuff_document_chain)
    

    def get_response(self, user_input: str):
        retriever_chain = chat_service.get_context_retriever_chain(st.session_state.vector_store)
        conversation_rag_chain = chat_service.get_conversational_rag_chain(retriever_chain)
        response = conversation_rag_chain.invoke({
            "chat_history": st.session_state.chat_history,
            "input": user_input
        })

        return response['answer']

    
chat_service = ChatService()