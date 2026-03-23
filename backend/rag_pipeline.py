from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from .pdf_loader import load_and_split_pdf
from .embeddings import get_embeddings
import os

BASE_DIR = os.path.dirname(__file__)
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")
PDF_PATH = os.path.join(BASE_DIR, "data", "AttentionAllYouNeed.pdf")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def format_sources(docs):
    return sorted(set(doc.metadata.get("page", 0) + 1 for doc in docs))

def initialize_rag():
    chunks = load_and_split_pdf(PDF_PATH)
    embeddings = get_embeddings()

    if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
        vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    else:
        vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH)

    llm = ChatGroq(model="llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert AI research assistant specializing in the 'Attention Is All You Need' paper. "
            "Answer ONLY based on the context below. Be concise and specific. "
            "If the answer is not in the context, say 'I don't have that information.'\n\n"
            "Context:\n{context}"
        )),
        ("human", "{input}"),
    ])

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return {"chain": chain, "retriever": retriever}
