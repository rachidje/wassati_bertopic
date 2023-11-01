import streamlit as st

st.set_page_config(layout="wide")

from streamlit_pages import descriptive_analysis, topic_analysis, sentiment_analysis, homepage

PAGES = {
    "Home": homepage,
    "Descriptive Analysis": descriptive_analysis,
    "Topic Analysis": topic_analysis,
    "Sentiment Analysis": sentiment_analysis
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()


# Custom footer workaround to overide default streamlit footer
footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Model constructed by <a href="https://wassati.com" >Wassati - Engaging Organizations </a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)