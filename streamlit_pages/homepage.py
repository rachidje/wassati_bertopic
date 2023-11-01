import streamlit as st
from streamlit_utils import *

def app():
    st.title("Schneider Electric Verbatim Analysis")

    st.write("""
    Welcome to your data analysis dashboard! This interactive tool is designed to help you explore and understand the data you’ve collected about your products.
    
    The data includes scores given by users for your products, ranging from 0 to 10, and recommendation scores from your clients, also on a scale of 0 to 10. Additionally, we have comments from users providing feedback or explaining their scores.
    This data is organized by geographical level, allowing us to analyze trends and patterns in different Zones, Clusters, and Account Countries.

    In this overview section, we’ll present some high-level insights from the data.
    Remember this is just the beginning of our data journey. As we delve deeper into the dashboard, we’ll uncover more detailed insights about specific topics, sentiments, and how they vary across different classes.
             
    """)