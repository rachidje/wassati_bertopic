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
             
    st.header("""**3 - Emotion-specific Analysis**""")

    st.write("""In this section, you can select a specific value for a more focused analysis. This section provides a detailed breakdown of the chosen value’s distribution globally, across different categories, and across the topics within a chosen category. This allows for a more targeted exploration of specific value responses in the reviews.""")

    st.markdown(f"<h3 style='text-align: left; color: black;'>Go deeper in the evolution of each value</h3>", unsafe_allow_html=True)
    st.write("""For that you will find below two barcharts.\n One represents the repartition of a specified human value within a group of your choice (like geographical filters, market segment filter or the repartition in time.\n The other chart is more precise, more specific. It still represents the repartition of a specified value within a group of your choice, adding one more information : the topics. You can through it study the repartition of an value per topic and per a group of your choice\n\n""")

    st.subheader('Single human value repartition')
    st.write("""Here we study the repartition of each value by a certain group.\n\n""")
    # Giving user options for selecting the value
    value = st.selectbox('Select the value you want to study',my_data["schwartz_values"])
    groupby_option = st.selectbox('Select the group you want to study the value on',groupby_options)

    # We define 3 columns in order to put the image in the second and then have it centered
    if groupby_option!='year' :
        time_period = st.selectbox('Select the period of time you want to study',my_data["year"])
        if time_period=="all_time":
            time_period=None
        fig = plot_barchart_distribution(data, groupby_option, time_period=time_period, percentage_by="Topic", filter_col="schwartz_label", filter_value=value, height=650, width=1300)
        st.plotly_chart(fig)

    elif groupby_option=="year":
        fig = plot_barchart_distribution(data, groupby_option, time_period=None, percentage_by="Topic", filter_col="schwartz_label", filter_value=value, height=650)
        st.plotly_chart(fig)


    st.subheader("Repartition of the human values within a subclass and topics")
    st.write("""Here we can track the repartition of a specific human value according to a specified data group.\n\n""")
    value = st.selectbox('Which value do you want to see the repartition ?',my_data["schwartz_values"])
    groupby_option = st.selectbox('With which class do you want to see the topic repartition of the value chosen?',groupby_options)

    st.subheader("Class-wise")    
    print_graph(f'dashboard/data/graphs/Schwartz_Analysis/repartition_per_topic/human_values_by_class/by_{groupby_option}/{value}_pct.html',height=750)
    st.subheader("Topic-wise")    
    print_graph(f'dashboard/data/graphs/Schwartz_Analysis/repartition_per_topic/human_values_by_class/by_{groupby_option}/{value}_class_pct.html',height=750)
    st.subheader("Repartition by levels")    
    value_sunburst = st.selectbox('Select one human value',my_data["schwartz_values"])
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        fig = sunburst(data, levels, color_sequence, unique_parent=True, class_column="schwartz_label", class_value=value_sunburst)
        st.plotly_chart(fig)
