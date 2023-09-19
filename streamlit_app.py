import os
import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components

# p = open("data/graphs/topic_merged_per_class_sentiment.html")
# components.html(p.read())
st.set_page_config(layout="wide")

st.title("Schneider Electric Verbatim Analysis")

@st.cache_data
def load_data():
    """
    Loads data from a CSV file.

    Returns:
    pandas.DataFrame: The loaded data.
    """
    data = pd.read_csv('data/csv_files/df_all_labelled.csv')
    return data

def print_graph(path, height=None, width=None):
    """
    Prints a graph from a specified file path.

    Parameters:
    path (str): The file path of the graph.
    height (int, optional): The height of the graph. Defaults to None.
    width (int, optional): The width of the graph. Defaults to None.

    Returns:
    None
    """
    graph = open(path)
    # get the extension
    extension = os.path.splitext(path)[1]
    if extension==".html":
        return components.html(graph.read(), height=height, width=width)
    elif extension==".png":
        return st.image(path)

def data_representation_buttons(session_var, button_col_freq, button_col_pct):
    """
    Creates two buttons for selecting data representation and updates the session state based on the selection.

    Parameters:
    session_var (str): The session state variable that stores the selected data representation.
    button_col_freq (streamlit.delta_generator.DeltaGenerator): The Streamlit column for the 'By Count' button.
    button_col_pct (streamlit.delta_generator.DeltaGenerator): The Streamlit column for the 'By Percentage' button.

    Returns:
    None
    """
    # Initialize session state for the selection
    if session_var not in st.session_state:
        st.session_state[session_var] = 'By Count'
    # Create buttons and handle selection
    if button_col_freq.button('By Count', key=session_var+"_freq"):
        st.session_state[session_var] = 'By Count'
    if button_col_pct.button('By Percentage', key=session_var+"_pct"):
        st.session_state[session_var] = 'By Percentage'

def print_freq_pct_choice(session_var, path, **kwargs): 
    """
    Prints the graph specified by the session variable.

    Parameters:
    session_var (str): The session state variable that determines which graph to print.
    path (str): The file path of the graph.
    **kwargs: Arbitrary keyword arguments for the print_graph function.

    Returns:
    None
    """
    extension = os.path.splitext(path)[1]
    root = os.path.splitext(path)[0]
    if st.session_state[session_var]== "By Count":
        print_graph(path, **kwargs)
    elif st.session_state[session_var]== "By Percentage":
        print_graph(root+"_pct"+extension, **kwargs)


data = load_data()
groupby_options = ['year', 'Zone', 'Clusters','Account Country', 'Market Segment']
# Store the parameters lists in a dictionary
my_data = {option: (np.insert(data[option].unique().astype('object'), 0, "all_time") if option == 'year' else data[option].unique()) for option in groupby_options}
# Add the merged_topics and emotions lists to the my_data dictionary
my_data['merged_topics'] = data['label'].unique()
my_data['emotions'] = data['single_emotion_label'].unique()

shorter_names={
    "single_emotion_label":"emotion",
    "sentiment_label":"sentiment",
    "Market Segment":"market",
    "Account Country":"country",
    "Zone":"zone",
    "Clusters":"cluster",
    "year":"year"
}

st.write("""
Here you will find many ways to investigate the schneider data through several forms of data visualization

**Have fun :)**
""")


st.header("Clustering des data")
st.write("""
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


# Custom footer workaround to overide default streamlit footer
footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Model constructed by <a href="https://wassati.com" >Wassati - Engaging Organizations </a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)