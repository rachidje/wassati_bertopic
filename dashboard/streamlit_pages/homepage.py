import streamlit as st
from utils.streamlit_utils import *

def app():
    st.title("Schneider Electric Verbatim Analysis")

    st.write("""
    Welcome to your data analysis dashboard!
    
    This interactive tool is designed to help you explore and understand the data you’ve collected about your products.
    <br>The data includes scores given by users for your products, ranging from 0 to 10, and recommendation scores from your clients, also on a scale of 0 to 10. Additionally, we have comments from users providing feedback or explaining their scores.
    This data is organized by geographical level, allowing us to analyze trends and patterns in different Zones, Clusters, and Account Countries.

    In this overview section, we’ll present some high-level insights from the data.
    Remember this is just the beginning of our data journey. As we delve deeper into the dashboard, we’ll uncover more detailed insights about specific topics, sentiments, and how they vary across different classes.
    <br><br><br><br>
    """, unsafe_allow_html=True)

    nb_scores = data["Overall Satisfaction"].count()
    nb_recommend_scores = data["Likelihood to Recommend (SE)"].count()
    nb_comments = len(data_comments_only)
    pct_comment_by_score = round(nb_comments/nb_scores*100,2)

    _,middle,_ = st.columns([1,1,1])
    with middle:
        st.markdown("<div style='text-align: center; font-size: 50px;'><strong>OVERVIEW</strong></div><br>", unsafe_allow_html=True)
    
    col1,col2 = st.columns([1,1])
    with col1:
        st.markdown("<div style='text-align: center; font-size: 50px;'><strong>55K</strong></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 20px;'>The data contains 55 072 individual 'Overall Satisfaction' scores</div>", unsafe_allow_html=True)
        st.write("<br><br>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align: center; font-size: 50px;'><strong>19K</strong></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 20px;'>The data contains 19 059 individual 'Likelihood to Recommend' scores</div>", unsafe_allow_html=True)
        st.write("<br><br>", unsafe_allow_html=True)

    _,middle,_ = st.columns([1,1,1])
    with middle:
        st.markdown("<br><div style='text-align: center; font-size: 30px;'><strong>Comments</strong></div><br><br>", unsafe_allow_html=True)

    col1,col2 = st.columns([1,1])
    with col1:
        _, subcol2, _= st.columns([1,2,1])
        with subcol2:
            st.write("Number of Comments")
            st.write(f'## {nb_comments}')
    with col2:
        _, subcol2, _= st.columns([1,3,1])
        with subcol2:
            st.write("Percentage of reviews with comments")
            st.write(f'## {pct_comment_by_score}%')
        st.progress(pct_comment_by_score/100)

    st.write("<br><br>", unsafe_allow_html=True)
    st.warning("we’ve taken all the comments from different columns and combined them into one text for our study. However, we didn’t include the comments from the “what is the customer feedback?” column because those comments are in various languages and haven’t been translated.")
