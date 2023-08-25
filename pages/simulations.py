# streamlit_app.py

import streamlit as st
import streamlit.components.v1 as components
from st_pages import add_page_title

@st.cache_data
def print_html(data_path):
    with open(data_path, 'r') as f:
        html_data = f.read()

    # Render the h1 block, contained in a frame of size 200x200.
    components.html(html_data, width=600, height=500)

add_page_title()

with st.expander('Colaboration network'):
    print_html('data/network_plot/colab_network.html')
with st.expander('Countinous Actors Plot'):
    print_html('data/network_plot/continous_antons_net.html')
with st.expander('Network with Interstitial Cluster'):
    print_html('data/network_plot/network_with_interstitial_cluster.html')
with st.expander('Network with new cluster'):
    print_html('data/network_plot/network_with_new_cluster.html')
with st.expander('New Discourse'):
    print_html('data/network_plot/new_discourse.html')
with st.expander('Colaboration outside own network'):
    print_html('data/network_plot/outside_form_colab_network.html')
with st.expander('Colaboration within own network'):
    print_html('data/network_plot/within_form_colab_network.html')

