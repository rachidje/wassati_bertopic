import streamlit as st
from streamlit_utils import *

def app():
    st.header("Topic Analysis")
    st.write("""
    Welcome to the Topic Analysis section of the dashboard. This section is designed to provide a detailed overview of the topics derived from the comments and how they are distributed across different classes (year, zone, clusters, etc.).""")
    
    st.info("""
    **What is clustering?**
    
    Clustering is a technique used to group similar data points together. In the context of Natural Language Processing (NLP), clustering can be used to identify patterns and relationships in large amounts of text data. This can be a challenging task, as language is complex and often ambiguous, and there are many different ways that text data can be represented and analyzed.

    Over the years, NLP has evolved significantly, with the rise of advanced machine learning algorithms and the availability of large amounts of data. These developments have enabled us to develop more sophisticated methods for clustering text data, using some of the most complex AI algorithms available. These state-of-the-art techniques can help us better understand the underlying structure of language and extract valuable insights from text data.""")
    
    col1, col2 = st.columns([1,1.7])
    with col1:
        st.markdown("<h3 style='text-align: center; color: black;'>Many very precise topics</h3>", unsafe_allow_html=True)
        print_graph('data/graphs/Clustering/global/topic_visualize_topics.html', height=750)
    with col2:
        st.markdown("<h3 style='text-align: center; color: black;'>The biggest 12 topics keywords</h3>", unsafe_allow_html=True)
        print_graph('data/graphs/Clustering/global/top_12_topics_barchart_viz.html', height=750)


    st.subheader('''Topics hierarchy''')
    st.write("""Let's ordered all those topics hierarchicaly\n\n""")
    print_graph('data/graphs/Clustering/hierarchy/topics_hierarchy.html', height=1050)


    st.subheader('Aggregated Topics')
    st.write(
        'Finally the analyzed reviews can be clustered into few categories using several AI algorithms combined:\n'
        '* Topic 1: **Delivery Deadlines** : challenges and strategies involved in managing delivery deadlines in logistics operations. \n'
        '* Topic 2: **Quotation and Pricing Strategies**. \n'
        '* Topic 3: **Touch Panels and Touch Screens** \n'
        '* Topic 4: **Frequency Converters** : frequency converters used in industrial applications and the technical support provided by manufacturers and suppliers \n'
        '* Topic 5: **Product Evaluation** : evaluate the quality, affordability and reliability of products and services. \n'
        '* Topic 6: **Automation Components** : hardware and software components used in industrial automation systems. \n'
        '* Topic 7: Reliability and Quality in **Customer Service and Support**. \n'
        '* Topic 8: **Problem Solving and Communication** : focus on the importance of being efficient, quick and precise when solving problems \n'
        '* Topic 9: **Assistance and Guidance**. \n'
        '* Topic 10: **Power Supply Issues**. \n'
        '* Topic 11: **Technical Support**. \n'
        '* Topic 12: Some **Positive Feedbacks** \n'
        )

    st.subheader('''Vizualize documents per aggregated topic''')
    st.write("""Let's regroup the many subtopics into the aggregated topics\n\n""")
    print_graph('data/graphs/Clustering/documents_viz/topic_merged_visualize_reduced_docs.html', height=750)


    st.subheader('''Wordcloud''')
    st.write("""Let's see how the aggregated topics are described through their corresponding wordcloud images\n\n""")
    # Giving user options for selecting the topic
    topic_option = st.selectbox('Select topic : which wordcloud do you want to see ?', my_data["merged_topics"])
    # Display two wordcloud images side by side.
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h4 style='text-align: center; color: grey;'>topic_option Wordcloud</h4>", unsafe_allow_html=True)
        st.image(f'data/wordclouds/topic_model_merged/{topic_option}.png')
    with col2:
        st.markdown(f"<h4 style='text-align: center; color: grey;'>topic_option Wordcloud with lemmatized words</h4>", unsafe_allow_html=True)
        st.image(f'data/wordclouds/topic_model_merged/{topic_option}_lemmatized.png') 


    st.subheader('''Topic Evolution''')
    st.write("""Let's check the topics evolution in time (by months)\n\n""")
    print_graph('data/graphs/Clustering/topic_in_time/topic_merged_time_by_months.html', height=500)


    st.subheader('''Heatmaps Graphics''')
    st.write("""Let's see how the topics are related to each other\n\n""")
    # Display two heatmap images side by side.
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='text-align: center; color: grey;'>The global topics relations</h4>", unsafe_allow_html=True)
        print_graph('data/graphs/Clustering/heatmap/topic_merged_heatmap.html', height=750)
    with col2:
        st.markdown("<h4 style='text-align: center; color: grey;'>The sub-topics relations</h4>", unsafe_allow_html=True)
        print_graph('data/graphs/Clustering/heatmap/topic_heatmap.html', height=750)


    st.subheader("Topic Repartition")
    st.write("""Let's study the repartition of the topics regarding some other groups information\n\n""")
    # Giving user options for selecting the class repartition
    groupby_option = st.selectbox('Select group : by which class do you want to see the topic repartition?',groupby_options)

    # Add buttons to choose for frequency or percentage for the representation of the data 
    _, col2, col3, _ = st.columns([3,1,1,7])
    data_representation_buttons("topic_repartition", col2, col3)
    # Produces topic_per_class barchart
    path = f'data/graphs/Clustering/topic_repartition/by_{groupby_option}/model_merged_per_{groupby_option}.html'
    print_freq_pct_choice("topic_repartition", path, height=750)
