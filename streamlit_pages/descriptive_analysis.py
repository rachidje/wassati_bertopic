import streamlit as st
from streamlit_utils import *
import copy 

def app():
    # Add a title and introduction text
    st.title("Descriptive Analysis")
    st.markdown("""
    Welcome to the Descriptive Analysis section of the dashboard. This section is designed to provide a detailed overview of the data, focusing on the distribution of scores and comments across different geographical areas and time periods.

    Here, you'll find visualizations such as:

    1. **Score Distribution by Class**: These charts show how product scores and recommendation scores are distributed across different classes (year, zone, clusters, etc.). They can help us understand how performance varies across different areas or periods.

    2. **Comment Fulfillment Rate by Class**: These charts show the rate of comment fulfillment for each class. They can help us understand where we're getting the most feedback and where there might be gaps.

    3. **Hierarchy Chart**: These charts show the total number of comments for each level. They give an idea of where most of the feedback is coming from.

    Feel free to explore these visualizations and gain insights into your data.
    """)

    # Create a copy of the dictionary
    my_data_copy = copy.deepcopy(my_data)
    # Use boolean indexing to create a new array without "all_time"
    my_data_copy['year'] = my_data_copy['year'][my_data_copy['year'] != 'all_time']

    tab1, tab2, tab3 = st.tabs(["Score Distribution", "Completion Rate", "Hierarchy Levels"])

                                        ### SCORE DISTRIBUTION ###
    with tab1:
        st.subheader('1. Score Distribution')
        # Add buttons to choose for score or recommendation score for the representation of the data 
        st.markdown("""Select here the score you want to study :""")
        subcols = st.columns([3,1,1,3])
        labels = ['Score', 'Recommendation Score']
        data_representation_buttons("score type", [subcols[1], subcols[2]], labels)

        # Score Distribution Global
        st.markdown("<h3 style='text-align: center;'><br>Global Score Distribution</h3>", unsafe_allow_html=True)
        _, col2, _ = st.columns([1,3,1])
        paths = ['data/graphs/Descriptive_Analysis/score_repartition/score_distribution.html',
                'data/graphs/Descriptive_Analysis/score_repartition/recommend_score_distribution.html']
        with col2:
            print_choice("score type", paths, labels, height=500, width=1000)

        # Score Distribution by Group
        st.markdown("<h3 style='text-align: center;'>Score Distribution by group</h3>", unsafe_allow_html=True)
        st.write("""Here we study the repartition of the score by a certain group.\n\n""")
        # Giving user options for selecting the group by 
        groupby_option = st.selectbox('Select the group you want to study the score distribution on',groupby_options)
        # Update the session state with the selected option
        st.session_state['groupby_option'] = groupby_option
        values = st.multiselect('Select the values you want to see the repartition',my_data_copy[groupby_option])

        # Call the function to create and print the chart
        if values:
            if st.session_state['score type'] == 'Score':
                fig = plots_score_distribution(data, 'Overall Satisfaction', st.session_state['groupby_option'], values_list=values, metric_type="percentage", merge=True, height=700, width=1300)
                st.plotly_chart(fig)
            else:
                fig = plots_score_distribution(data, 'Likelihood to Recommend (SE)', st.session_state['groupby_option'], values_list=values, metric_type="percentage", merge=True, height=700, width=1300)
                st.plotly_chart(fig)
        else:
            st.warning("Please select at least one value to see the score distribution chart.")

                                        ### COMMENTS FILL RATE ###
    with tab2:
        st.subheader('\n\n2. Comments completion rate')
        groupby_option = st.selectbox('Select the group you want to study the comments completion rate',groupby_options)
        fig = filling_data_barchart(data, groupby_option, 'non_empty_rows', height=600, width=1500)
        st.plotly_chart(fig)
        groupby_options2 = [item for item in groupby_options if item != groupby_option]
        groupby_option2 = st.selectbox(f"Select the secondary group you want to study alongside the '{groupby_option}' group for a more detailed comments completion rate analysis",groupby_options2)
        values = st.multiselect(f"Select the specific values for the first group '{groupby_option}' you want to see the completion rate",my_data_copy[groupby_option])

        # Call the function to create and print the chart
        if values:
            fig = filling_data_barcharts(data, [groupby_option, groupby_option2], 'non_empty_rows', values_list=values, height=800, width=1300)
            st.plotly_chart(fig)
        else:
            st.warning("Please select at least one value to see the completion rate chart.")

                                        ### HIERARCHY LEVELS: SUNBURST###
    with tab3:
        st.subheader('\n\n3. Hierarchy levels for Comments')
        _, col2, _ = st.columns([1,3,1])
        with col2:
            # print_graph('data/graphs/Descriptive_Analysis/fullfilling_rate/sunburst.html', height=800, width=800)
            fig = sunburst(data_comments_only, levels, color_sequence, unique_parent=True)
            st.plotly_chart(fig)

