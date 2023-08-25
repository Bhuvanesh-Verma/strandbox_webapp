import json
from collections import defaultdict
from tempfile import NamedTemporaryFile

from dotenv import load_dotenv
import streamlit as st
from langchain import PromptTemplate

from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
import qdrant_client
import os
from langchain.llms import GPT4All

#@st.cache_resource(show_spinner="Initializing embedding model...")
def get_embedding_model():
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings
#@st.cache_resource(show_spinner="Preparing Vector store...")
def get_vector_store(collection_name):
    client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    embeddings = get_embedding_model()


    vector_store = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    return vector_store
#@st.cache_resource(show_spinner="Preparing QA pipeline...")
def get_model(_vector_store):
    # create chain
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Use three sentences maximum and keep the answer as concise as possible. 
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    llm = GPT4All(model="/Users/bhuvanesh/Documents/models/wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin", max_tokens=2048)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=_vector_store.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    return qa


def clear_text():
    st.session_state["temp"] = st.session_state["text"]
    st.session_state["text"] = ""

def init_session_states():
    if "temp" not in st.session_state:
        st.session_state["temp"] = ""

def display_interaction_area(qa, type='local'):
    init_session_states()

    user_question = st.text_input("What do you want to know ?", key="text", on_change=clear_text)
    user_question = st.session_state['temp']

    if user_question:

        st.write(f"Question: {user_question}")
        answer = qa(user_question)
        st.write(f"Answer: {answer['result']}")
        # docs = defaultdict()
        st.write('Source Documents')
        if type=='local':
            for doc in answer["source_documents"]:
                st.write(doc.page_content)
        else:
            for doc in answer["source_documents"]:
                with st.expander(f"{doc.metadata['title']}"):
                    st.write(doc.page_content)
                    st.write(doc.metadata)
def run_from_backend():
    st.header("Ask your questions from desired journal 💬")

    collection_map = {'EIST': 'eist', 'RSOG': 'rsog', 'SUS-SCI': 'sus_sci', 'Collection of 217': '217'}
    ops = [None] + list(collection_map.keys())
    option = st.selectbox(
        'Select a journal',
        (ops))

    if option is not None:
        # create vector store
        vector_store = get_vector_store(collection_name=collection_map[option])

        qa = get_model(vector_store)
        display_interaction_area(qa, type='db')


def run_locally():
    uploaded_file = st.file_uploader("Choose a pdf file", accept_multiple_files=False)
    if uploaded_file is not None:
        with NamedTemporaryFile(dir='.', suffix='.pdf') as f:
            f.write(uploaded_file.getbuffer())
            loader = PyPDFLoader(f.name)
            pdf_docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=['. '])
            documents = text_splitter.split_documents(pdf_docs)
            embeddings = get_embedding_model()
            vector_store = Qdrant.from_documents(
                documents,
                embeddings,
                location=":memory:",  # Local mode with in-memory storage only
                collection_name=f'{f.name}',
            )
            qa = get_model(vector_store)
            display_interaction_area(qa)

@st.cache_data
def get_data(uploaded_file):
    with open('data/research_structure.json', 'r') as f:
        data = json.load(f)

    if uploaded_file is not None:
        with NamedTemporaryFile(dir='.', suffix='.pdf') as f:
            f.write(uploaded_file.getbuffer())
            loader = PyPDFLoader(f.name)
            pdf_docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=['. '])
            documents = text_splitter.split_documents(pdf_docs)
            embeddings = get_embedding_model()
            vector_store = Qdrant.from_documents(
                documents,
                embeddings,
                location=":memory:",  # Local mode with in-memory storage only
                collection_name=f'{f.name}',
            )

    return data, vector_store

def create_tab(data, db):
    cats = [None] + list(data.keys())
    option = st.selectbox(
        'Select a category',
        (cats))
    if option is not None:
        question = data[option]
        st.write(question)
        docs = db.similarity_search(question)

        for i, doc in enumerate(docs):
            st.write(f'Answer-{i+1}')
            st.write(doc.page_content)

def main():
    load_dotenv()

    st.set_page_config(page_title="Interact with Strandbox")
    st.title("Interact with Strandbox")

    uploaded_file = st.file_uploader("Choose a pdf file", accept_multiple_files=False)
    data, vector_store = get_data(uploaded_file)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(list(data.keys()))

    with tab1:
        create_tab(data["Research Question"], vector_store)

    with tab2:
        create_tab(data["Analytical Framework"], vector_store)

    with tab3:
        create_tab(data["Research Method"], vector_store)

    with tab4:
        create_tab(data["Data Sources"], vector_store)

    with tab5:
        create_tab(data["Time Horizon"], vector_store)



if __name__ == '__main__':
    main()