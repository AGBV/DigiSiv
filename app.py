import streamlit as st

# st.set_page_config(page_title="DigiSiv", page_icon=":material/edit:")
pg = st.navigation(
    [
        st.Page("exercise00/mandelbrot.py"),
        st.Page("exercise01/M01.py"),
        st.Page("exercise02/M02.py"),
        st.Page("exercise04/M03.py"),
        st.Page("exercise05/M04.py"),
    ]
)
pg.run()
