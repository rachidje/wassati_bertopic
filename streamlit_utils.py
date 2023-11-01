import streamlit.components.v1 as components
import streamlit as st
import os 
import pandas as pd
import numpy as np

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