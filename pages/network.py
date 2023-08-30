# streamlit_app.py
import json

import streamlit as st
import streamlit.components.v1 as components
from st_pages import add_page_title
from os import listdir
import os
import plotly.io as pio

@st.cache_data
def print_html(data_path, width=1000, height=1000):
    with open(data_path, 'r') as f:
        html_data = f.read()

    # Render the h1 block, contained in a frame of size 200x200.
    components.html(html_data, width=width, height=height)

st.title('Strandbox')
st.subheader('📡 Networks')

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

"""
with st.expander('General Networks'):
    jsonfiles = [f for f in listdir('data/strandmix') if f.endswith('.json')]
    names = {json_file.split('.json')[0]: os.path.join('data/strandmix', json_file) for json_file in jsonfiles}
    options = [None] + list(names.keys())
    option = st.selectbox(
        'Select a category',
        (options))
    if option is not None:
        st.info('Please wait for figures to load. Press \u2921 for better view.')
        with open(names[option], 'r') as f:
            data = json.load(f)
        fig = pio.from_json(data)
        st.plotly_chart(fig, use_container_width=True)
        #print_html(names[option], width=1000, height=800)
        #webbrowser.open(names[option])

"""