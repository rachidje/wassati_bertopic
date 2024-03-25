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
    We’ve used advanced techniques to cluster the reviews into 7 distinct topics and performed sentiment analysis to identify sentiments and emotions. This page is divided into three main sections, each providing a unique perspective on the data.""")
             
    st.header("""**3 - Emotion-specific Analysis**""")

    st.write("""In this section, you can select a specific emotion for a more focused analysis. This section provides a detailed breakdown of the chosen emotion’s distribution globally, across different categories, and across the topics within a chosen category. This allows for a more targeted exploration of specific emotional responses in the reviews.""")

    st.markdown(f"<h3 style='text-align: left; color: black;'>Go deeper in the evolution of each emotion</h3>", unsafe_allow_html=True)
    st.write("""For that you will find below two barcharts.\n One represents the repartition of a specified emotion within a group of your choice (like geographical filters, market segment filter or the repartition in time.\n The other chart is more precise, more specific. It still represents the repartition of a specified emotion within a group of your choice, adding one more information : the topics. You can through it study the repartition of an emotion per topic and per a group of your choice\n\n""")

    st.subheader('Single emotion repartition')
    st.write("""Here we study the repartition of each emotion by a certain group.\n\n""")
    # Giving user options for selecting the emotion
    emotion = st.selectbox('Select the emotion you want to study',my_data["emotions"])
    groupby_option = st.selectbox('Select the group you want to study the emotion on',groupby_options)

    # We define 3 columns in order to put the image in the second and then have it centered
    if groupby_option!='year' :
        time_period = st.selectbox('Select the period of time you want to study',my_data["year"])
        if time_period=="all_time":
            time_period=None
        fig = plot_barchart_distribution(data, groupby_option, time_period=time_period, percentage_by="Topic", filter_col="single_emotion_label", filter_value=emotion, height=650, width=1300)
        st.plotly_chart(fig)

    elif groupby_option=="year":
        fig = plot_barchart_distribution(data, groupby_option, time_period=None, percentage_by="Topic", filter_col="single_emotion_label", filter_value=emotion, height=650)
        st.plotly_chart(fig)


    st.subheader("Repartition of the emotions within a subclass and topics")
    st.write("""Here we can track the repartition of a specific emotion according to a specified data group.\n\n""")
    emotion = st.selectbox('Which emotion do you want to see the repartition ?',my_data["emotions"])
    groupby_option = st.selectbox('With which class do you want to see the topic repartition of the emotion chosen?',groupby_options)

    st.subheader("Class-wise")    
    print_graph(f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/emotion_by_class/by_{groupby_option}/new_{emotion}_pct.html',height=750)
    st.subheader("Topic-wise")    
    print_graph(f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/emotion_by_class/by_{groupby_option}/new_{emotion}_class_pct.html',height=750)
    st.subheader("Repartition by levels")    
    emotion_sunburst = st.selectbox('Select one emotion',my_data["emotions"])
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        fig = sunburst(data, levels, color_sequence, unique_parent=True, class_column="single_emotion_label", class_value=emotion_sunburst)
        st.plotly_chart(fig)
