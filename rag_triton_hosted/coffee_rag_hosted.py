import os
from langchain import hub
from langchain.schema import StrOutputParser
from langchain_community.vectorstores import faiss
from langchain_core.runnables import RunnablePassthrough
from triton_llm import TritonLLM
from credential_utilties.environment import setEnvironmentVariables
from embeddings.embeddings_wrapper import HuggingFaceEmbeddings

vectorstore = None
prompt = None

def init():
    setEnvironmentVariables()
    global vectorstore
    global prompt

    embeddings = HuggingFaceEmbeddings(model_id = "multi-qa-mpnet-base-dot-v1")
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR", default=""),"coffee_embeddings")
    vectorstore = faiss.FAISS.load_local(model_path, embeddings, allow_dangerous_deserialization=True)
    prompt = hub.pull("rlm/rag-prompt")

def run(query):
    retriever = vectorstore.as_retriever()

    llm = TritonLLM()
    def format_docs(docs):
        return "\n\n ".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    ragtext = rag_chain.invoke(query)
    return [ragtext]
    

if __name__ == '__main__':
     init()
     print(run('what is latte'))
