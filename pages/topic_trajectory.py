# streamlit_app.py
import time

import streamlit as st
import spacy_streamlit
from collections import defaultdict
from st_pages import Page, show_pages, add_page_title, show_pages_from_config
import pandas as pd
import streamlit.components.v1 as components

@st.cache_data
def create_expanders(data_path, type):
    if type == 1:
        title = "EIST"
    elif type == 2:
        title = "RSOG"
    elif type == 3:
        title = "Sus-Sci"
    elif type == 4:
        title = "3 journals"
    else:
        st.error(f'No such type: {type} exist')
    with st.expander(title):
        with open(data_path, 'r') as f:
            html_data = f.read()

        # Render the h1 block, contained in a frame of size 200x200.
        components.html(html_data, width=1000, height=400)

st.title('Strandbox')
st.write('Topic trajectories over the time')

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Hot", "Cold", "Wallflowers", "Reviving", "Evergreen"])

with tab1:
    create_expanders('data/trends/eist_hot.html', 1)
    create_expanders('data/trends/rsog_hot.html', 2)
    create_expanders('data/trends/sussci_hot.html', 3)
    create_expanders('data/trends/3_journals_hot.html', 4)


with tab2:
    create_expanders('data/trends/rsog_cold.html', 2)

    create_expanders('data/trends/3_journals_cold.html', 4)


with tab3:
    create_expanders('data/trends/eist_wallflowers.html', 1)
    create_expanders('data/trends/rsog_wallflowers.html', 2)
    create_expanders('data/trends/sussci_wallflowers.html', 3)
    create_expanders('data/trends/3_journals_wallflowers.html', 4)

with tab4:
    create_expanders('data/trends/eist_reviving.html', 1)
    create_expanders('data/trends/rsog_reviving.html', 2)
    create_expanders('data/trends/sussci_reviving.html', 3)
    create_expanders('data/trends/3_journals_reviving.html', 4)

with tab5:
    create_expanders('data/trends/eist_evergreen.html', 1)
    create_expanders('data/trends/rsog_evergreen.html', 2)
    create_expanders('data/trends/sussci_evergreen.html', 3)
    create_expanders('data/trends/3_journals_evergreen.html', 4)