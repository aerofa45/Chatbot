from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory  # 
from dotenv import load_dotenv
from src.prompt import *
import os


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "chat-bot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

chatModel = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# Conversation Memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


# Store retrieved documents into memory
def store_doc_memory(memory, response):
    if "context" in response:
        docs = response["context"]
        for d in docs:
            text = d.page_content.strip()
            if text:
                memory.chat_memory.add_ai_message(f"RETRIEVED_DOC: {text}")


@app.route("/")
def index():
    return render_template('chatbot.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]

    # NEW: Store user message
    memory.chat_memory.add_user_message(msg)

    # Run RAG
    response = rag_chain.invoke({"input": msg})
    answer = response["answer"]

    # NEW: Store AI answer
    memory.chat_memory.add_ai_message(answer)

    # NEW: Store retrieved document chunks
    store_doc_memory(memory, response)

    return str(answer)


#  NEW OPTIONAL ENDPOINT: Reset memory if needed
@app.route("/reset", methods=["POST"])
def reset_memory():
    memory.clear()
    return "Memory cleared!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
