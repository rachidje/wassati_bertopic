import streamlit as st
from streamlit_utils import *
import copy 

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
    Here, you'll find visualizations such as:

    1. **Count Frequency Charts**: These charts show the total number of comments for each sentiment or emotion. They give an idea of the overall emotional tone of the feedback.

    2. **Topic-wise Percentage Bar Charts**: These charts show what portion of comments each sentiment or emotion represents within each topic. It's like asking, "Out of all the comments about topic A, what percentage were positive?" This type of chart is useful for understanding how sentiments vary across different topics.

    3. **Class-wise Percentage Bar Charts**: These charts show how much each class (year, zone, etc.) contributes to a particular sentiment or emotion. It's like asking, "What percentage of positive comments were made in 2023?" This can help us understand which sentiments are most prevalent in each class.

    4. **Deep Dive into Specific Emotions**: These visualizations allow for a deeper analysis of specific emotions, showing how they vary across different topics and classes.""")

    # Create a copy of the dictionary
    my_data_copy = copy.deepcopy(my_data)
    # Use boolean indexing to create a new array without "all_time"
    my_data_copy['year'] = my_data_copy['year'][my_data_copy['year'] != 'all_time']

    tab1, tab2, tab3 = st.tabs(["Global Sentiment", "Sentiment by Topic", "Specific Sentiment"])

    with tab1:
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


    with tab2:
        st.subheader('Sentiments and Emotions Repartition By Topic')
        st.write("""Let's study the repartition by topic of the sentiments and emotions.\n\n""")
        
        st.subheader("Topic-wise")
        col1, col2 = st.columns([1,2.3])
        with col1:
            # st.markdown("<h4 style='text-align: center; color: grey;'>By Sentiment</h4>", unsafe_allow_html=True)
            print_graph('data/graphs/Sentiment_Analysis/by_sentiment/repartition_per_topic/global/model_merged_per_sentiment_pct.html', height=750)
        with col2:
            # st.markdown("<h4 style='text-align: center; color: grey;'>By Emotion</h4>", unsafe_allow_html=True)
            print_graph('data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/global/model_merged_per_emotion_pct.html', height=750)

        st.subheader("Class-wise")
        col1, col2 = st.columns([1,2.3])
        with col1:
            # st.markdown("<h4 style='text-align: center; color: grey;'>By Sentiment</h4>", unsafe_allow_html=True)
            print_graph('data/graphs/Sentiment_Analysis/by_sentiment/repartition_per_topic/global/model_merged_per_sentiment_class_pct.html', height=750)
        with col2:
            # st.markdown("<h4 style='text-align: center; color: grey;'>By Emotion</h4>", unsafe_allow_html=True)
            print_graph('data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/global/model_merged_per_emotion_class_pct.html', height=750)


        st.subheader("Emotions Repartition according to a subclass AND the topics")
        st.write("""Let's check the repartition of emotions according to a specified data group AND according to the topics.\n\n""")
        groupby_option = st.selectbox('By which class do you want to see the emotion topic repartition?',groupby_options)
        # Propose to the user to choose one of the values that exist in his precedent chosen class
        options = [x for x in my_data[groupby_option] if groupby_option != "year" or x != "all_time"]
        value = st.selectbox(f'By which {shorter_names[groupby_option]} do you want to see the emotion topic repartition?',options)
        col1, col2, col3, col4 = st.columns([3,1,1,5])
        data_representation_buttons("singlevalue_group_by_emotions_and_topic", [col2, col3], ['By Count', 'By Percentage'])
        paths = [f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/class_by_emotions/by_{groupby_option}/{value}.html',
                f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/class_by_emotions/by_{groupby_option}/{value}_pct.html']
        print_choice("singlevalue_group_by_emotions_and_topic", paths, ['By Count', 'By Percentage'], height=750)

    with tab3:
        texte = "Go deeper in the evolution of each emotion"
        st.markdown(f"<h3 style='text-align: left; color: black;'>{texte}</h3>", unsafe_allow_html=True)
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


        st.subheader("Repartition of the emotions within a subclass")
        st.write("""Here we can track the repartition of a specific emotion according to a specified data group.\n\n""")
        emotion = st.selectbox('Which emotion do you want to see the repartition ?',my_data["emotions"])
        groupby_option = st.selectbox('With which class do you want to see the topic repartition of the emotion chosen?',groupby_options)
        col1, col2, col3, col4 = st.columns([3,1,1,5])
        data_representation_buttons("single_emotion_by_group_and_topic", [col2, col3], ['By Count', 'By Percentage'])
        paths = [f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/emotion_by_class/by_{groupby_option}/{emotion}.html',
                f'data/graphs/Sentiment_Analysis/by_emotion/repartition_per_topic/emotion_by_class/by_{groupby_option}/{emotion}_pct.html']
        print_choice("single_emotion_by_group_and_topic", paths, ['By Count', 'By Percentage'], height=750)

