import streamlit as st
from dashboard.v1.utils.streamlit_utils import *

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

    st.header("""**1 - Global Sentiment Analysis**""")

    st.write("""In this section, you’ll find an overview of the sentiment distribution across all reviews. This includes the proportion of positive, negative, and neutral sentiments, as well as the distribution of the 27 identified emotions. To provide a more detailed view, we also present these distributions according to specific categories. This allows you to understand the overall sentiment and emotional landscape of the reviews.""")

    st.subheader('Sentiments and Emotions Repartition')
    col1, col2 = st.columns([1,2.3])
    with col1:
        fig = plot_barchart_distribution(data, "sentiment_label", time_period=None, percentage_by="Topic", width=450, height=750)
        st.plotly_chart(fig)
    with col2:
        fig = plot_barchart_distribution(data, "single_emotion_label", time_period=None, percentage_by="Topic", width=1100, height=750)
        st.plotly_chart(fig)

    st.subheader('Sentiments and Emotions Repartition By Class')
    groupby_option = st.selectbox('Select the group you want to study the sentiments/emotions on',groupby_options)
    values = st.multiselect('Select the values you want to see the repartition',my_data[groupby_option])

    col1, col2 = st.columns([1,2.3])
    if values :
        if groupby_option!='year' :
            time_period = st.selectbox('Select the period of time you want to study',my_data["year"])
            if time_period=="all_time":
                time_period=None
            with col1:
                fig = plot_barcharts_distribution(data, "sentiment_label", groupby_option, values_list=values, time_period=time_period, percentage_by="Topic", merge=True, width=450, height=750)
                st.plotly_chart(fig)
            with col2:
                fig = plot_barcharts_distribution(data, "single_emotion_label", groupby_option, values_list=values, time_period=time_period, percentage_by="Topic", merge=True, width=1100, height=750)
                st.plotly_chart(fig)
        else:
            with col1:
                fig = plot_barcharts_distribution(data, "sentiment_label", groupby_option, values_list=values, time_period=None, percentage_by="Topic", merge=True, width=450, height=750)
                st.plotly_chart(fig)
            with col2:
                fig = plot_barcharts_distribution(data, "single_emotion_label", groupby_option, values_list=values, time_period=None, percentage_by="Topic", merge=True, width=1100, height=750)
                st.plotly_chart(fig)
    else :
        st.warning("Please select at least one value to see the sentiment and emotion distribution chart.")  
