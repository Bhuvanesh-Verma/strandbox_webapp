# streamlit_app.py

import streamlit as st

from PIL import Image
from st_pages import show_pages_from_config

@st.cache_data
def create_block_image(img_path, title):
    image = Image.open(img_path)
    new_image = image.resize((600, 400))
    st.image(new_image)
    st.subheader(title)

st.set_page_config(layout="wide")
st.title('Strandbox')
st.write('A study on three journals, Environmental Innovation and Societal Transitions (EIST), Research in Sociology of Organizations (RSOG)'
         ' and Sustainability Science (SusSci).')



show_pages_from_config('.streamlit/pages.toml')

col1, col2 = st.columns(2)


with col1:
    create_block_image("data/img/topics.jpg", 'Topics')

with col2:
    create_block_image("data/img/trajectory.jpg", 'Topic Trajectories')

col3, col4 = st.columns(2)

with col3:
    create_block_image("data/img/network.jpg", 'Networks')

with col4:
    create_block_image("data/img/simulations.jpg", 'Simulations')