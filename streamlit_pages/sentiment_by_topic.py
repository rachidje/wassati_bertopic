import streamlit as st
from streamlit_utils import *

def app():
    st.header("Sentiment Analysis")
    st.write("""
    Welcome to the Sentiment Analysis section of the dashboard. This section is designed to delve into the sentiments and emotions expressed in the comments.""")

    st.info("""
    **What is 'Sentiment Analysis'?**
    
    Sentiment analysis is a technique used to determine the emotional tone behind a piece of text. It can be used to identify whether the text expresses a positive, neutral, or negative sentiment. Emotion analysis goes deeper and can identify specific emotions such as approval, disappointment, anger, and more.
    
    This can be useful for understanding how people feel about a particular topic or product. Sentiment analysis is a complex field that involves natural language processing and machine learning techniques, but the results can provide valuable insights into the emotions expressed in text.\n\n
    """)

    st.write("""
    We’ve used advanced techniques to cluster the reviews into 12 distinct topics and performed sentiment analysis to identify sentiments and emotions. This page is divided into three main sections, each providing a unique perspective on the data.""")

    st.header("""**2 - Sentiment/Emotion and Topic**""")

    st.write("""This section delves deeper into the sentiment and emotion distribution across the 12 identified topics. Here, you’ll find charts depicting the sentiment and emotion distribution for each topic. Additionally, we provide topic-wise and class-wise percentage charts to give you a more granular understanding of the sentiment distribution within each topic and category.""")

    st.subheader('**2.1** - Sentiments and Emotions Repartition By Topic')
    st.write("""Let's study the repartition by topic of the sentiments and emotions.\n\n""")
    
    st.subheader("Class-wise")    
    col1, col2 = st.columns([1,2.3])
    with col1:
        # st.markdown("<h4 style='text-align: center; color: grey;'>By Sentiment</h4>", unsafe_allow_html=True)
        print_graph('data/graphs/Sentiment_Analysis/by_sentiment/repartition_per_topic/global/new_model_merged_per_sentiment_pct.html', width=700, height=750)
    with col2:
        # st.markdown("<h4 style='text-align: center; color: grey;'>By Emotion</h4>", unsafe_allow_html=True)
        print_graph('data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/global/new_model_merged_per_emotion_pct.html', width=1150, height=750)

    st.subheader("Topic-wise")
    col1, col2 = st.columns([1,1])
    with col1:
        # st.markdown("<h4 style='text-align: center; color: grey;'>By Sentiment</h4>", unsafe_allow_html=True)
        print_graph('data/graphs/Sentiment_Analysis/by_sentiment/repartition_per_topic/global/new_model_merged_per_sentiment_class_pct.html', width=700, height=750)
    with col2:
        # st.markdown("<h4 style='text-align: center; color: grey;'>By Emotion</h4>", unsafe_allow_html=True)
        print_graph('data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/global/new_model_merged_per_emotion_class_pct.html', width=1150, height=750)


    st.subheader("**2.2** - Emotions Repartition according to a subclass AND the topics")
    groupby_option = st.selectbox('By which class do you want to see the emotion topic repartition?',groupby_options)
    # Propose to the user to choose one of the values that exist in his precedent chosen class
    options = [x for x in my_data[groupby_option] if groupby_option != "year" or x != "all_time"]
    value = st.selectbox(f'By which {shorter_names[groupby_option]} do you want to see the emotion topic repartition?',options)
 
    st.subheader("Class-wise")
    print_graph(f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/class_by_emotions/by_{groupby_option}/new_{value}_pct.html',width=1500, height=750)
    st.subheader("Topic-wise")
    print_graph(f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/class_by_emotions/by_{groupby_option}/new_{value}_class_pct.html',width=1500, height=750)
