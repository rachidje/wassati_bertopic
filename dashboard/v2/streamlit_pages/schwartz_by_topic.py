import streamlit as st
from dashboard.v2.utils.streamlit_utils import *

def app():
    st.header("Human Value Analysis")
    st.write("""
    Welcome to the Human Value Analysis section of the dashboard. This section is designed to delve into the human values expressed in the comments.""")

    st.info("""
    **What is 'Human Value Analysis'?**
    
    This section studies the (often implicit) human values behind natural language arguments, such as to have freedom of thought or to be broadminded. Values are commonly accepted answers to why some option is desirable in the ethical sense and are thus essential both in realworld argumentation and theoretical argumentation frameworks. \n\n
    """)

    st.write("""
    We’ve used advanced techniques to cluster the reviews into 20 distinct values and performed our analysis to identify them. This page is divided into three main sections, each providing a unique perspective on the data.""")

    st.header("""**2 - Human Values and Topic**""")

    st.write("""This section delves deeper into the human values distribution across the 7 identified topics. Here, you’ll find charts depicting the human values distribution for each topic. Additionally, we provide topic-wise and class-wise percentage charts to give you a more granular understanding of the values distribution within each topic and category.""")

    st.subheader('**2.1** - Human Values Repartition By Topic')
    st.write("""Let's study the repartition by topic of the human values.\n\n""")
    
    st.subheader("Class-wise")    
    # st.markdown("<h4 style='text-align: center; color: grey;'>By Emotion</h4>", unsafe_allow_html=True)
    print_graph('dashboard/data/graphs/Schwartz_Analysis/repartition_per_topic/global/model_merged_per_humanvalue_pct.html', width=1150, height=750)

    st.subheader("Topic-wise")
    # st.markdown("<h4 style='text-align: center; color: grey;'>By Emotion</h4>", unsafe_allow_html=True)
    print_graph('dashboard/data/graphs/Schwartz_Analysis/repartition_per_topic/global/model_merged_per_humanvalue_class_pct.html', width=1150, height=750)


    st.subheader("**2.2** - Values Repartition according to a subclass AND the topics")
    groupby_option = st.selectbox('By which class do you want to see the human values topic repartition?',groupby_options)
    # Propose to the user to choose one of the values that exist in his precedent chosen class
    options = [x for x in my_data[groupby_option] if groupby_option != "year" or x != "all_time"]
    value = st.selectbox(f'By which {shorter_names[groupby_option]} do you want to see the value topic repartition?',options)
 
    st.subheader("Class-wise")
    print_graph(f'dashboard/data/graphs/Schwartz_Analysis/repartition_per_topic/class_by_human_values/by_{groupby_option}/{value}_pct.html',width=1500, height=750)
    st.subheader("Topic-wise")
    print_graph(f'dashboard/data/graphs/Schwartz_Analysis/repartition_per_topic/class_by_human_values/by_{groupby_option}/{value}_class_pct.html',width=1500, height=750)
