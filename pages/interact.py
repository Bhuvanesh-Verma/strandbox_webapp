from collections import defaultdict

import streamlit as st
import json

@st.cache_data
def load_data():
    with open('data/strandqa.json', 'r') as f:
        data = json.load(f)
    f.close()
    return data

@st.cache_data
def get_doc_names(doc2data):
    docs = list(doc2data.keys())
    names = defaultdict(str)
    for doc in docs:
        source = doc2data[doc]["Research Question"]["Main Question"]["source"][0]
        name = f'{source["metadata"]["title"]} --- {source["metadata"]["doi"]}'
        names[doc] = name
    return names

def create_tab(docdata):
    cats = [None] + list(docdata.keys())
    option = st.selectbox(
        'Select a category',
        (cats))
    if option is not None:
        ques = docdata[option]['question']
        st.write(ques)
        ans = docdata[option]['result']
        metadata = docdata[option]['source'][0]['metadata']
        st.write(ans)
        for i, src in enumerate(docdata[option]['source']):
            with st.expander(f'Source {i+1}'):
                st.write(src['content'])

        st.divider()

        with st.expander("Metadata"):
            st.write(metadata)


st.set_page_config(page_title="Interact with Strandbox")
st.title("Interact with Strandbox")

data = load_data()

name_map = {'EIST':'eist', 'RSOG':'rsog', 'Sus-Sci':'sussci'}

options = [None] + list(name_map.keys())
option = st.selectbox(
    'Choose a Journal',
    (options))

if option is not None:
    journal = name_map[option]

    id2name = get_doc_names(data[journal])
    name2id = {name:id for id, name in id2name.items()}
    sample_articles = [None] + list(name2id.keys())
    name = st.selectbox(
        'Select a sample document',
        (sample_articles))


    if name is not None:
        docid = name2id[name]
        doc_data = data[journal][docid]

        tab1, tab2, tab3, tab4, tab5 = st.tabs(list(doc_data.keys()))

        with tab1:
            create_tab(doc_data["Research Question"])

        with tab2:
            create_tab(doc_data["Analytical Framework"])

        with tab3:
            create_tab(doc_data["Research Method"])

        with tab4:
            create_tab(doc_data["Data Sources"])

        with tab5:
            create_tab(doc_data["Time Horizon"])