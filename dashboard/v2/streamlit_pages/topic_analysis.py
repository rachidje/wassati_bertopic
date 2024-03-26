import streamlit as st
from dashboard.v2.utils.streamlit_utils import *

def app():
    st.header("Topic Analysis")
    st.write("""
    Welcome to the Topic Analysis section of the dashboard. This section is designed to provide a detailed overview of the topics derived from the comments and how they are distributed across different classes (year, zone, clusters, etc.).""")

    tab1, tab2, tab3 = st.tabs(["Topic Discovery", "Topic Analysis", "Topic Distribution"])

    with tab1:
        st.info("""
        **What is clustering?**
        
        Clustering is a technique used to group similar data points together. In the context of Natural Language Processing (NLP), clustering can be used to identify patterns and relationships in large amounts of text data. This can be a challenging task, as language is complex and often ambiguous, and there are many different ways that text data can be represented and analyzed.

        Over the years, NLP has evolved significantly, with the rise of advanced machine learning algorithms and the availability of large amounts of data. These developments have enabled us to develop more sophisticated methods for clustering text data, using some of the most complex AI algorithms available. These state-of-the-art techniques can help us better understand the underlying structure of language and extract valuable insights from text data.""")

        st.write("""In this section, you'll see a series of charts that will help us understand the topics derived from the reviews. The goal of this analysis is to identify patterns and relationships in the reviews. By understanding these topics, we can gain valuable insights into what people are saying.<br><br>
                 First, we have a 2D plot representing the numerous topics identified by our IA model. This plot shows the distance between topics, helping us understand how similar or different they are.<br>
                 Next to this, you'll see barcharts showing the top 5 keywords for the best topics. These keywords give us a quick understanding of what each topic is about.<br><br>""", unsafe_allow_html=True)
         
        col1, col2 = st.columns([1,1.7])
        with col1:
            st.markdown("<h3 style='text-align: center; color: black;'>Many very precise topics</h3>", unsafe_allow_html=True)
            print_graph('dashboard/data/graphs/Clustering/global/new_topic_visualize_topics.html', height=750)
        with col2:
            st.markdown("<h3 style='text-align: center; color: black;'>The biggest 12 topics keywords</h3>", unsafe_allow_html=True)
            print_graph('dashboard/data/graphs/Clustering/global/new_top_12_topics_barchart_viz.html', height=750)


        st.subheader('''Topics hierarchy''')
        st.write("""Below there's a Hierarchical Clustering chart. This chart shows the relationships between the many base topics, giving us a bird's eye view of the topic structure.<br><br>""", unsafe_allow_html=True)
        print_graph('dashboard/data/graphs/Clustering/hierarchy/new_topics_hierarchy.html', height=750)


        st.subheader('Aggregated Topics')
        # st.write(
        #     'Finally, based on the previous charts and several AI algorithms combined, we have defined 12 final merged topics that we decided to keep. These are the topics that we believe best represent the reviews:\n'
        #     '* Topic 1: **Delivery Deadlines** : challenges and strategies involved in managing delivery deadlines in logistics operations. \n'
        #     '* Topic 2: **Quotation and Pricing Strategies**. \n'
        #     '* Topic 3: **Touch Panels and Touch Screens** \n'
        #     '* Topic 4: **Frequency Converters** : frequency converters used in industrial applications and the technical support provided by manufacturers and suppliers \n'
        #     '* Topic 5: **Product Evaluation** : evaluate the quality, affordability and reliability of products and services. \n'
        #     '* Topic 6: **Automation Components** : hardware and software components used in industrial automation systems. \n'
        #     '* Topic 7: Reliability and Quality in **Customer Service and Support**. \n'
        #     '* Topic 8: **Problem Solving and Communication** : focus on the importance of being efficient, quick and precise when solving problems \n'
        #     '* Topic 9: **Assistance and Guidance**. \n'
        #     '* Topic 10: **Power Supply Issues**. \n'
        #     '* Topic 11: **Technical Support**. \n'
        #     '* Topic 12: Some **Positive Feedbacks** \n'
        #     )

        st.write(
            'Finally, based on the previous charts and several AI algorithms combined, we have defined 12 final merged topics that we decided to keep. These are the topics that we believe best represent the reviews:\n'
            '* Topic 1: **Product Quality & Sales** \n'
            '* Topic 2: **UPS & Touch Panels** : Technical Support and Maintenance for UPS Systems and Touch Panels \n'
            '* Topic 3: **Quotations & Offers** : Quotations and Offers Management \n'
            '* Topic 4: **Customer Service & Delivery** : Customer Service and Delivery Scheduling \n'
            '* Topic 5: **Inverters & Drives Support**  \n'
            '* Topic 6: **Tech Support & Problem Resolution** \n'
            '* Topic 7: **Communication, Guidance & Feedback**. \n'
            )

    with tab2:
        st.write("This section provides a detailed overview of the 7 topics we identified in the Topic Discovery section. You'll see in more detail what the topics correspond to and how they've evolved over time.\n\n")
        st.subheader('''Vizualize documents per aggregated topic''')
        st.write("First, we have a 2D plot that visualizes the reviews in a 2D space per topic. Each point on this plot represents a review, and the distance between points indicates how similar the topics of the reviews are. Points that are close together are reviews that discuss similar topics.")
        print_graph('dashboard/data/graphs/Clustering/documents_viz/new_topic_merged_visualize_reduced_docs.html', height=750, width=1300)

        st.subheader('''Wordcloud''')
        st.info("A wordcloud is a visual representation of text data where the size of each word indicates its importance. So, the larger the word in the wordcloud, the more strongly it defines the topic.")
        st.write("""Let's see how the aggregated topics are described through their corresponding wordcloud images\n\n""")
        # Giving user options for selecting the topic
        topic_option = st.selectbox('Select topic : which wordcloud do you want to see ?', my_data["merged_topics"])
        # Display two wordcloud images side by side.
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<h4 style='text-align: center; color: grey;'>topic_option Wordcloud</h4>", unsafe_allow_html=True)
            st.image(f'dashboard/data/wordclouds/new_topic_model_merged/{topic_option}.png')
        # with col2:
        #     st.markdown(f"<h4 style='text-align: center; color: grey;'>topic_option Wordcloud with lemmatized words</h4>", unsafe_allow_html=True)
        #     st.image(f'dashboard/data/wordclouds/topic_model_merged/{topic_option}_lemmatized.png') 

        st.write("<br><br>", unsafe_allow_html=True)
        st.subheader('''Topic Evolution''')
        st.write("""Let's check the topics evolution in time (by months). This chart shows how the prevalence of each topic has changed over time. Each line represents a topic, and the height of the line at any point in time indicates how prevalent that topic was among the reviews at that time.\n\n""")
        print_graph('dashboard/data/graphs/Clustering/topic_in_time/new_topic_merged_time_by_months.html', height=500)


        st.subheader('''Heatmaps Graphics''')
        st.info("A heatmap is like a table or grid, where each cell is colored based on its value. Imagine a weather map showing temperatures - areas with similar temperatures have the same color. A heatmap works in a similar way, but it’s usually used to show how much two things are related to each other.")
        st.write("""Let's see how the topics are related to each other\n\n""")
        st.write('**How to interpret the heatmaps chart ?**\n\n')
        st.write('Each cell shows how similar two customer service components are. The darker the color, the more similar they are.\n'
                 'For example, “Customer Support” and “Product Evaluation” are very similar, as indicated by the dark blue color. On the other hand, “Positive feedback” and “Power Supply Issues” are not very similar, as indicated by the light green color. This helps us understand which components are closely related.')

        # Display two heatmap images side by side.
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='text-align: center; color: grey;'>The global topics relations</h4>", unsafe_allow_html=True)
            print_graph('dashboard/data/graphs/Clustering/heatmap/new_topic_merged_heatmap.html', height=750)
        with col2:
            st.markdown("<h4 style='text-align: center; color: grey;'>The sub-topics relations</h4>", unsafe_allow_html=True)
            print_graph('dashboard/data/graphs/Clustering/heatmap/new_topic_heatmap.html', height=750)

    with tab3:
        st.subheader("Topic Repartition")
        st.write("This section is designed to provide a detailed overview of how the topics we identified in the 'Topic Discovery' section are distributed across different categories.<br><br>The main feature of this section is two barcharts that show the distribution of topics for a selected category. The category can be chosen from a selection box and could represent different aspects such as year, geographical zone, country, or market segment.<br><ul><li><strong>Class-wise Percentage Barchart:</strong> This chart shows how much each class (year, zone, etc.) contributes to a particular topic. It’s like asking, “What percentage of comments about topic A were made in 2023?” This can help us understand which topics are most relevant for each class.</li><li><strong>Topic-wise Percentage Barchart:</strong> Each bar in the chart represents a topic, and the length of the bar indicates the percentage of that topic within the selected category. The topics are color-coded for easy identification, and you can see the exact topic each color represents in the legend. The hovertext of each bar shows the count frequency, which is the raw number of occurrences of each topic.</li></ul>By exploring this chart, you can gain valuable insights into the prevalence and significance of each topic within different contexts.<br><br>", unsafe_allow_html=True)

        st.subheader('''1. Class-wise Percentage''')
        st.info("**Class-wise Percentage**: This is calculated as the frequency of each class within each topic. It answers questions like 'What percentage of comments about topic A were made in 2023?' or 'What percentage of comments about topic B were made in Zone X?'")
        st.write("""**Keys to analyze the Class-wise Percentage Barchart**: 
- This chart should be interpreted topic by topic to understand the distribution of each topic across different classes. For each topic, the chart shows the percentage of comments within each class, providing a clear picture of how discussion on that topic is distributed.

- When multiple topics are added to the chart, it allows for a comparative analysis of topic distributions. Since the percentages provide a normalized basis for comparison, it’s possible to directly compare the distribution of different topics across the same classes. This can highlight interesting contrasts and similarities in the way different topics are discussed within each class.

- **For example**, if Topic A and Topic B are both added to the chart, you might notice that Topic A has a high percentage of comments in 2023, while Topic B has a more even distribution across several years. This could indicate that Topic A was a trending topic in 2023, while Topic B has been a consistent point of discussion over time.

- **In summary**, the key to effectively using this chart is to analyze one topic at a time, and then use the percentage-based comparison to understand the relative distribution of multiple topics.""")
        # Giving user options for selecting the class repartition
        groupby_option = st.selectbox('Select group : by which class do you want to see the repartition?',groupby_options)
        print_graph(f'dashboard/data/graphs/Clustering/topic_repartition/by_{groupby_option}/new_model_merged_per_{groupby_option}_pct.html', width=1500, height=750)

        st.subheader('''2. Topic-wise Percentage''')
        st.info("**'Topic-wise Percentage'**: This is calculated as the frequency of each topic within each class. In other words, it answers questions like 'What percentage of comments in 2023 were about topic A?' or 'What percentage of comments in Zone X were about topic B?'")

        st.write("""**Keys to analyze the Topic-wise Percentage Barchart**:
- This chart provides a comprehensive view of the distribution of comments across different topics within a selected class. Each segment of a stacked bar represents a topic, and its length indicates the percentage of comments about that topic within the chosen class.
                 
- **For instance**, if you select the class '2023', the chart will show the distribution of topics discussed in that year. A larger segment for Topic A would mean that a higher percentage of comments in 2023 were about Topic A. The color-coding and the legend aid in identifying each topic quickly and easily.

- When multiple classes are selected, the chart allows for a comparative analysis of topic distributions across these classes. For example, comparing the stacked bars for '2023' and '2022' could reveal shifts in discussion trends over the years.

- The hovertext feature provides additional information by showing the raw count frequency, which is the actual number of occurrences of each topic. This can give you a sense of the volume of discussion around each topic.

- **In summary**, the Topic-wise Percentage Barchart, with its stacked presentation, is a powerful tool for understanding the prominence of different topics within each class and tracking changes over time or across different areas.""")

        # Giving user options for selecting the class repartition
        groupby_option = st.selectbox('Select group : by which class do you want to see the topic repartition?',groupby_options)
        print_graph(f'dashboard/data/graphs/Clustering/topic_repartition/by_{groupby_option}/new_model_merged_per_{groupby_option}_class_pct.html', width=1500, height=750)



