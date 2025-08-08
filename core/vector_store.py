from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import yaml
import os

VECTOR_STORE_DIR = "vector_store"

# Load configuration from config.yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def initialize_vector_store(data):
    """
    Initializes the vector store with the provided data.
    """
    if not data:
        raise ValueError("No data provided to initialize the vector store.")
        return None
    
    try:
        # Initialize embeddings using Google Generative AI
        embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=config["google_api_key"],
            model="models/embedding-001" 
        )
        # Create chunks of text from the data
        texts = []
        for item in data:
            # Divide the text into paragraphs
            paragraphs = item['content'].split('\n\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    texts.append(paragraph.strip())
        
        print("\n=== Chunks to index ===")
        for i, text in enumerate(texts, 1):
            print(f"\nChunk {i}:")
            print("-" * 30)
            print(text)
            print("-" * 30)
        
        # Ensure the vector store directory exists
        os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

        # Initialize the vector store with the texts and embeddings
        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory=VECTOR_STORE_DIR
        )
        print(f"Vector store initialized and persisted at {VECTOR_STORE_DIR}")
        return vector_store
    
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        return None 

def load_vector_store():
    """
    Loads the vector store from the persisted directory.
    """
    try:
        # Ensure the vector store directory exists
        if not os.path.exists(VECTOR_STORE_DIR):
            raise FileNotFoundError(f"Vector store directory {VECTOR_STORE_DIR} does not exist.")
        
        # Load the vector store from the persisted directory
        vector_store = Chroma(persist_directory=VECTOR_STORE_DIR)
        print(f"Vector store loaded from {VECTOR_STORE_DIR}")
        return vector_store
    
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None
