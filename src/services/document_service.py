from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

class DocumentService:
    def get_pdf_text(self, pdf_docs: list[any]) -> str:
        text = ""
        for pdf in pdf_docs:
            loader = PdfReader(pdf)
            for page in loader.pages:
                text += page.extract_text()
        
        return text
    
    def get_text_chunks(self, raw_text: str) -> list[str]:
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(raw_text)

        return chunks


document_service = DocumentService()