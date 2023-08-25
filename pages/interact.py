import json
from tempfile import NamedTemporaryFile

import streamlit as st
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant


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
@st.cache_data
def get_data(uploaded_file):
    with open('data/research_structure.json', 'r') as f:
        data = json.load(f)


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
    if uploaded_file is not None:
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