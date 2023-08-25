# streamlit_app.py

import streamlit as st
import streamlit.components.v1 as components
from st_pages import add_page_title

@st.cache_data
def print_html(data_path):
    with open(data_path, 'r') as f:
        html_data = f.read()

    # Render the h1 block, contained in a frame of size 200x200.
    components.html(html_data, width=600, height=400)

add_page_title()

with st.expander('EIST'):
    print_html('data/topic_networks/topic_network_eist_antons.html')

with st.expander('RSOG'):
    print_html('data/topic_networks/topic_network_rsog_antons.html')

with st.expander('Sus-Sci'):
    print_html('data/topic_networks/topic_network_sussci_antons.html')


with st.expander('3 journals'):
    tab1, tab2, tab3, tab4 = st.tabs(["Full Network", "Weight > 1", "Weight > 3", "Weight > 5"])

    with tab1:
        print_html('data/topic_networks/topic_network_3_journals_antons.html')

    with tab2:
        print_html('data/topic_networks/topic_network_3_journals_antons_wgt1+.html')

    with tab3:
        print_html('data/topic_networks/topic_network_3_journals_antons_wgt3+.html')

    with tab4:
        print_html('data/topic_networks/topic_network_3_journals_antons_wgt5+.html')