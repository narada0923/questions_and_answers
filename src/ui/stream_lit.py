import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from src.services.store_service import store_service
from src.services.chat_service import chat_service
from src.services.document_service import document_service
from streamlit_modal import Modal

class StreamLit:    
    def print_conversation(self):
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)

    def init_page(self):
        st.set_page_config(page_title="Crawl and chat", page_icon="🤖")
        st.title("Scrape or provide data and ask anything")

        modal = Modal(
            "PDF Preview", 
            key="pdf-report",
            
            # Optional
            padding=20,    # default value
            max_width=744  # default value
        )  
        if 'processed' not in st.session_state:
            st.session_state.processed = False

        with st.sidebar:
            st.header("Settings ⚙️")
            url = st.text_input("Webste url")
            st.subheader("Your documents 📄")
            pdf_docs = st.file_uploader("Upload your PDFs here and click process", accept_multiple_files=True)

            if st.button("Process"):
                if pdf_docs is None or len(pdf_docs) == 0:
                    st.warning(body="Please upload any pdf file!", icon="🚨")
                else:
                    with st.spinner("Processing"):
                        st.session_state.processed = True
                        raw_text = document_service.get_pdf_text(pdf_docs)
                        text_chunks = document_service.get_text_chunks(raw_text)

                        if "vector_store" not in st.session_state:
                            st.session_state.vector_store = store_service.get_vectorstore_from_document(text_chunks)

            if pdf_docs is not None and len(pdf_docs) > 0:
                for doc in pdf_docs:
                    if st.button(f"{doc.name}"):
                        raw_text_s = document_service.get_pdf_text([doc])
                        st.session_state.selected_chunks = document_service.get_text_chunks(raw_text_s)
                        
                        modal.open()
            
                if modal.is_open():
                    with modal.container():
                        st.write(st.session_state.selected_chunks)
                     


        if (url is None or url == "") and (pdf_docs is None or len(pdf_docs) == 0):
            st.info("Please enter a website url or upload any file")
        else:
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [
                    AIMessage(content="Hello, I'm a bot. How can I help you?")
                ]
                self.print_conversation()
            
            if isinstance(url, str) and url != "":
                if "vector_store" not in st.session_state:
                    st.session_state.vector_store = store_service.get_vectorstore_from_url(url)

            user_query = st.chat_input("Type your message here...")
            if user_query is not None and user_query != "":  
                if not st.session_state.processed and pdf_docs is not None and len(pdf_docs) > 0:
                    st.warning(body="Please process uploaded documents", icon="🚨")
                else:
                    response = chat_service.get_response(user_query)
                    st.session_state.chat_history.append(HumanMessage(content=user_query))     
                    st.session_state.chat_history.append(AIMessage(content=response))
                    self.print_conversation()

stream_lit = StreamLit()