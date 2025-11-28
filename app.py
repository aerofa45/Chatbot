from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from src.prompt import *
import os


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# ---------------- Embeddings + Index ----------------
embeddings = download_hugging_face_embeddings()

index_name = "chat-bot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# ---------------- Model ----------------
chatModel = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{chat_history}\n\nUser: {input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# ---------------- Memory ----------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


# ---------------- Memory Wrapper ----------------
def run_with_memory(user_input):
    """Add memory → run RAG → save memory."""
    
    # Load past memory
    chat_history = memory.load_memory_variables({})["chat_history"]

    # Convert chat history messages into text block
    history_text = "\n".join(
        f"User: {m.content}" if m.type == "human" else f"Assistant: {m.content}"
        for m in chat_history
    )

    # Run RAG with memory included
    response = rag_chain.invoke({
        "input": user_input,
        "chat_history": history_text   # passed into prompt
    })

    answer = response["answer"]

    # Save new turn to memory
    memory.save_context(
        {"input": user_input},
        {"output": answer}
    )

    return answer


# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template('chatbot.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("User:", msg)

    answer = run_with_memory(msg)

    print("Bot:", answer)
    return str(answer)


# Optional reset
@app.route("/reset", methods=["POST"])
def reset():
    memory.clear()
    return "Memory cleared."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
