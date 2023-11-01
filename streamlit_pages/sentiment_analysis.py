import streamlit as st
from streamlit_utils import *

def app():
    st.header("Sentiment Analysis")
    st.write("""
            Sentiment analysis is a technique used to determine the emotional tone behind a piece of text. It can be used to identify whether the text expresses a positive, neutral, or negative sentiment. Emotion analysis goes deeper and can identify specific emotions such as approval, disappointment, anger, and more. This can be useful for understanding how people feel about a particular topic or product. Sentiment analysis is a complex field that involves natural language processing and machine learning techniques, but the results can provide valuable insights into the emotions expressed in text.\n\n
            """)

    
    st.subheader('Sentiments and Emotions Repartition By Topic')
    st.write("""Let's study the global repartition by topic of the sentiments and emotions.\n\n""")


    col1, col2 = st.columns([1,2.3])
    with col1:
        st.markdown("<h4 style='text-align: center; color: grey;'>By Sentiment</h4>", unsafe_allow_html=True)
        # Add buttons to choose for frequency or percentage for the representation of the data 
        subcol1, subcol2, subcol3, subcol4 = st.columns([1,1,1,1])
        data_representation_buttons("sentiment_by_topic_global", subcol2, subcol3)
        path = 'data/graphs/Sentiment_Analysis/by_sentiment/repartition_per_topic/global/model_merged_per_sentiment.html'
        print_freq_pct_choice("sentiment_by_topic_global", path, height=750)
    with col2:
        st.markdown("<h4 style='text-align: center; color: grey;'>By Emotion</h4>", unsafe_allow_html=True)
        # Add buttons to choose for frequency or percentage for the representation of the data 
        subcol1, subcol2, subcol3, subcol4 = st.columns([3,1,1,3])
        data_representation_buttons("emotion_by_topic_global", subcol2, subcol3)
        path = 'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/global/model_merged_per_emotion.html'
        print_freq_pct_choice("emotion_by_topic_global", path, height=750)


    st.subheader('Single emotion repartition')
    st.write("""Here we study the repartition of each emotion by a certain group.\n\n""")
    # Giving user options for selecting the emotion
    emotion = st.selectbox('Select the emotion you want to study',my_data["emotions"])
    groupby_option = st.selectbox('Select the group you want to study the emotion on',groupby_options)

    # We define 3 columns in order to put the image in the second and then have it centered
    if groupby_option=='Zone' or groupby_option=='Clusters' or groupby_option=='Account Country' or groupby_option=='Market Segment' :
        time_period = st.selectbox('Select the period of time you want to study',my_data["year"])
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            subcol1, subcol2, subcol3, subcol4 = st.columns([1,1,1,1])
            data_representation_buttons("single_emotion_repartition", subcol2, subcol3)
            path = f'data/graphs/Sentiment_Analysis/by_emotion/repartition/by_{groupby_option}/{emotion}_{time_period}.png'
            print_freq_pct_choice("single_emotion_repartition", path, height=750)

    elif groupby_option=="year":
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            subcol1, subcol2, subcol3, subcol4 = st.columns([2,1,1,2])
            data_representation_buttons("single_emotion_repartition_year", subcol2, subcol3)
            path = f'data/graphs/Sentiment_Analysis/by_emotion/repartition/by_{groupby_option}/{emotion}.png'
            print_freq_pct_choice("single_emotion_repartition_year", path, height=750)


    texte = """Go deeper in the evolution of each emotion. 
    For that you will find below two barcharts.\n
    One represents the repartition of a specified emotion within a group of your choice (like geographical filters, market segment filter or the repartition in time.\n
    The other chart is more precise, more specific. It still represents the repartition of a specified emotion within a group of your choice, adding one more information : the topics. You can through it study the repartition of an emotion per topic and per a group of your choice\n\n"""
    st.markdown(f"<h3 style='text-align: left; color: black;'>{texte}</h3>", unsafe_allow_html=True)

    st.subheader("Repartition of the emotions within a subclass")
    st.write("""Here we can track the repartition of a specific emotion according to a specified data group.\n\n""")
    emotion = st.selectbox('Which emotion do you want to see the repartition ?',my_data["emotions"])
    groupby_option = st.selectbox('With which class do you want to see the topic repartition of the emotion chosen?',groupby_options)
    col1, col2, col3, col4 = st.columns([3,1,1,5])
    data_representation_buttons("single_emotion_by_group_and_topic", col2, col3)
    path = f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/emotion_by_class/by_{groupby_option}/{emotion}.html'
    print_freq_pct_choice("single_emotion_by_group_and_topic", path, height=750)


    st.subheader("Emotions Repartition according to a subclass AND the topics")
    st.write("""Let's check the repartition of emotions according to a specified data group AND according to the topics.\n\n""")
    groupby_option = st.selectbox('By which class do you want to see the emotion topic repartition?',groupby_options)
    # Propose to the user to choose one of the values that exist in his precedent chosen class
    options = [x for x in my_data[groupby_option] if groupby_option != "year" or x != "all_time"]
    value = st.selectbox(f'By which {shorter_names[groupby_option]} do you want to see the emotion topic repartition?',options)
    col1, col2, col3, col4 = st.columns([3,1,1,5])
    data_representation_buttons("singlevalue_group_by_emotions_and_topic", col2, col3)
    path = f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/class_by_emotions/by_{groupby_option}/{value}.html'
    print_freq_pct_choice("singlevalue_group_by_emotions_and_topic", path, height=750)