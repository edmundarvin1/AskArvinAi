
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Load the PDF and split into chunks
def load_vectorstore():
    loader = PyPDFLoader("data/ARVIN_DE_LEON.pdf")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=GPT4AllEmbeddings(),
        persist_directory="vectorstore/"
    )
    return vectorstore

# Initialize vectorstore
vectorstore = load_vectorstore()

# Load the LLM
llm = OllamaLLM(
    model="phi3:mini",
    base_url="http://127.0.0.1:11434",
    callbacks=[StreamingStdOutCallbackHandler()]
)

# Create the QA Chain
template = """You are a virtual assistant for Arvin's professional portfolio. Arvin 
is a data scientist with a background in computer science and a passion for machine
learning. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an 
answer. sentences maximum and keep the answer as concise as possible.

{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
)

# Handle queries
def query_model(query: str):
    result = qa_chain.invoke({"query": query})
    print(result)
    return result["result"]


if __name__ == "__main__":
    query_model("Did arvin work in brightbid?")
