from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import GoogleGenerativeAI
from core.vector_store import load_vector_store
from langchain.prompts import PromptTemplate
import yaml
from core.prompts import SYSTEM_TEMPLATE

# Load configuration from config.yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def handle_query(query, messages):
    # Initialize the LLM
    llm=GoogleGenerativeAI(   
        google_api_key=config["google_api_key"],
        model="gemini-1.5-flash",  
        temperature=0.2,
        max_output_tokens=1024
    )
    
    #Retrieve the vector store
    vector_store = load_vector_store()

    #Augment the prompt with context from the vector store
    prompt = PromptTemplate(template=SYSTEM_TEMPLATE, input_variables=["context", "question", "chat_history"])

    #Generate the conversational retrieval chain
    chain=ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3}),
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
        verbose=True
    )

    # Format the chat history for the chain
    formatted_history = []
    for msg in messages[1:]:
        if isinstance(msg, dict) and msg["role"] == "user":
            formatted_history.append((msg["content"], ""))

    try:
        result=chain.invoke({
            "question": query,
            "chat_history": formatted_history
        })
        return result['answer']
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Lo siento, ocurrió un error al procesar tu solicitud."