import os
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
import streamlit as st

# Create directory for vector DB
os.makedirs("vector_db", exist_ok=True)

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])
        self.vector_store = None
        self.init_vector_store()
    
    def init_vector_store(self):
        # Check if vector store exists, if not create it
        try:
            self.vector_store = Chroma(
                collection_name="anaptyss_docs",
                embedding_function=self.embeddings,
                persist_directory="vector_db"
            )
            print(f"Vector store loaded with {self.vector_store._collection.count()} documents")
        except Exception as e:
            print(f"Creating new vector store: {e}")
            self.vector_store = Chroma(
                collection_name="anaptyss_docs",
                embedding_function=self.embeddings,
                persist_directory="vector_db"
            )
            self.populate_from_docs()
    
    def populate_from_docs(self):
        """Load documents from the docs directory"""
        try:
            # Load documents from docs directory
            loader = DirectoryLoader("docs/", glob="**/*.md", loader_cls=TextLoader)
            documents = loader.load()
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)
            
            # Add to vector store
            self.vector_store.add_documents(chunks)
            self.vector_store.persist()
            print(f"Added {len(chunks)} document chunks to vector store")
        except Exception as e:
            print(f"Error populating vector store: {e}")
    
    def similar_docs(self, query, k=3):
        """Find most similar documents to the query"""
        if not self.vector_store:
            return []
        
        docs = self.vector_store.similarity_search(query, k=k)
        return docs
