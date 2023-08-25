import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

@st.cache_data
def create_expanders(data_path, type):
    if type == 1:
        title = "Topics"
    elif type == 2:
        title = "Descriptive Stats"
    elif type == 3:
        title = "Temporal Stats"
    elif type == 4:
        title = "Topics over articles"
    elif type == 5:
        title = "Verbs Analysis in Articles"
    else:
        st.error(f'No such type: {type} exist')
    with st.expander(title):
        if type == 4:
            st.image(data_path)
        elif type == 5:
            # Read file and keep in variable
            with open(data_path, 'r') as f:
                html_data = f.read()

            # Render the h1 block, contained in a frame of size 200x200.
            components.html(html_data, width=1000, height=1000)
        else:
            data = pd.read_csv(data_path)
            st.write(data)

st.title('Strandbox')
st.write('Topic Modelling results')
tab1, tab2, tab3, tab4 = st.tabs(["EIST", "RSOG", "Sus-Sci", "All 3"])

with tab1:
    create_expanders('data/tables/eist_topics.csv', 1)

    create_expanders('data/tables/descriptive_stats_eist.csv', 2)

    create_expanders('data/tables/eist_temp_dev_trajc.csv', 3)

    create_expanders('data/heatmaps/eist.png', 4)

    create_expanders('data/chord_chart/eist_chord.html', 5)


with tab2:
    create_expanders('data/tables/rsog_topics.csv', 1)

    create_expanders('data/tables/descriptive_stats_rsog.csv', 2)

    create_expanders('data/tables/rsog_temp_dev_trajc.csv', 3)

    create_expanders('data/heatmaps/rsog.png', 4)

    create_expanders('data/chord_chart/rsog_chord.html', 5)

with tab3:
    create_expanders('data/tables/sus-sci_topics.csv', 1)

    create_expanders('data/tables/descriptive_stats_sussci.csv', 2)

    create_expanders('data/tables/sussci_temp_dev_trajc.csv', 3)

    create_expanders('data/heatmaps/sussci.png', 4)

    create_expanders('data/chord_chart/ss_chord.html', 5)

with tab4:
    create_expanders('data/tables/3_journals_topics.csv', 1)

    create_expanders('data/tables/descriptive_stats_3_journals.csv', 2)

    create_expanders('data/tables/3_journals_temp_dev_trajc.csv', 3)

    create_expanders('data/heatmaps/3_journals.png', 4)