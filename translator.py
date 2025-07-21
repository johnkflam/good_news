import os
from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import argparse

class DocumentTranslator:
    def __init__(self, api_key=None, model_name="gpt-3.5-turbo"):
        """
        Initialize the document translator
        
        Args:
            api_key: OpenAI API key (can also be set as environment variable)
            model_name: OpenAI model to use for translation
        """
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.1,  # Low temperature for consistent translation
            max_tokens=2000
        )
        
        # Translation prompt template
        self.translation_prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            You are a professional translator. Translate the following English text to Hindi.
            Maintain the original meaning, tone, and formatting as much as possible.
            Provide only the Hindi translation without any additional commentary.
            
            English text:
            {text}
            
            Hindi translation:
            """
        )
        
        self.translation_chain = LLMChain(
            llm=self.llm,
            prompt=self.translation_prompt
        )


        # self.translation_chain = self.llm | self.translation_prompt
    
    def load_document(self, file_path):
        """
        Load document based on file extension
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of Document objects
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        elif file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension in ['.docx', '.doc']:
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        return loader.load()
    
    def split_text(self, documents, chunk_size=1000, chunk_overlap=100):
        """
        Split documents into smaller chunks for better translation
        
        Args:
            documents: List of Document objects
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of Document objects (chunks)
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

        if isinstance(documents,str):
            return text_splitter.split_text(documents)
        else:
            return text_splitter.split_documents(documents)
    
    def translate_chunk(self, text_chunk):
        """
        Translate a single text chunk
        
        Args:
            text_chunk: Text to translate
            
        Returns:
            Translated text
        """
        try:
            result = self.translation_chain.run(text=text_chunk)
            return result.strip()
        except Exception as e:
            print(f"Error translating chunk: {e}")
            return f"[Translation Error: {text_chunk[:50]}...]"

    def translate_text(self, text, chunk_size=1000):
        if len(text) > chunk_size:
            print('splitting text')
            chunks = self.split_text(text, chunk_size=chunk_size)
        else:
            chunks = [text]

        print(f'text: {text}, size: {len(text)}')

        translated_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"Translating chunk {i+1}/{len(chunks)}...")
            translated_text = self.translate_chunk(chunk)
            translated_chunks.append(translated_text)
        
        # Combine all translated chunks
        full_translation = "\n\n".join(translated_chunks)

        return full_translation
    
    def translate_document(self, file_path, output_path=None, chunk_size=1000):
        """
        Translate entire document from English to Hindi
        
        Args:
            file_path: Path to input document
            output_path: Path for output file (optional)
            chunk_size: Size of text chunks for translation
            
        Returns:
            Translated text
        """
        print(f"Loading document: {file_path}")
        
        # Load the document
        documents = self.load_document(file_path)
        
        # Split into chunks if document is large
        if len(documents[0].page_content) > chunk_size:
            print("Splitting document into chunks...")
            chunks = self.split_text(documents, chunk_size=chunk_size)
        else:
            chunks = documents
        
        print(f"Translating {len(chunks)} chunk(s)...")
        
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"Translating chunk {i+1}/{len(chunks)}...")
            translated_text = self.translate_chunk(chunk.page_content)
            translated_chunks.append(translated_text)
        
        # Combine all translated chunks
        full_translation = "\n\n".join(translated_chunks)
        
        # Save to file if output path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_translation)
            print(f"Translation saved to: {output_path}")
        
        return full_translation