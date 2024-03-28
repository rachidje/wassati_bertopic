import streamlit as st
from streamlit_utils import *

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

    st.header("""**1 - Global Human Value Analysis**""")

    st.write("""In this section, you’ll find an overview of the human value distribution across all reviews. To provide a more detailed view, we also present these distributions according to specific categories. This allows you to understand the overall human values landscape of the reviews.""")

    st.subheader('Human Value Repartition')

    fig = plot_barchart_distribution(data, "schwartz_label", time_period=None, percentage_by="Topic", width=1100, height=750)
    st.plotly_chart(fig)

    st.subheader('Human Value Repartition By Class')
    groupby_option = st.selectbox('Select the group you want to study the human values on',groupby_options)
    values = st.multiselect('Select the values you want to see the repartition',my_data[groupby_option])

    if values :
        if groupby_option!='year' :
            time_period = st.selectbox('Select the period of time you want to study',my_data["year"])
            if time_period=="all_time":
                time_period=None
            fig = plot_barcharts_distribution(data, "schwartz_label", groupby_option, values_list=values, time_period=time_period, percentage_by="Topic", merge=True, width=1100, height=750)
            st.plotly_chart(fig)
        else:
            fig = plot_barcharts_distribution(data, "schwartz_label", groupby_option, values_list=values, time_period=None, percentage_by="Topic", merge=True, width=1100, height=750)
            st.plotly_chart(fig)
    else :
        st.warning("Please select at least one value to see the humn values distribution chart.")  
