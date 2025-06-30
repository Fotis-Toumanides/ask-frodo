from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from vector import md_rag
import os
import streamlit as st


ollama_url = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
model = OllamaLLM(model="llama3.2", base_url=ollama_url)

template = """
Your name is 'Frodo' and you are a character in the book of the Markdown files. These files are your past adventures, so you answer the questions based on these Markdown files, like you are remembering.

Here are some relevant documents: {documents}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

md_files = "./lord-of-rings"
retriever = md_rag(
    source_directory=md_files, db_path="chroma_md_db", collection_name="tech_files"
)
print("Retriever ready.")

st.title("Lord Of The Rings")
# while True:
# ================= # Initialize chat history # ========================== #
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================ # Display messages from history # ====================== #
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# print("\n-------------------------------")
# question = input("Ask your question (q to quit): ")

# ================ # React to user input # ====================== #
quest = st.chat_input("Ask me about my adventure...")
question = str(quest)

if question:  # walrus checks if it's not none and assigns it to the prompt variable
    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

# Add user message to chat history
st.session_state.messages.append({"role": "user", "content": question})

docs = retriever.invoke(question)
result = chain.invoke({"documents": docs, "question": question})
# Assistant response
# response = f"echo: {question}"
with st.chat_message("assistant"):
    st.markdown(result)
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": result})
