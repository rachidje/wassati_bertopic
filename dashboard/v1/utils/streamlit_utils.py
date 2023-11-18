import streamlit.components.v1 as components
import streamlit as st 
import os 
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from itertools import cycle
import plotly.subplots as sp
import colorsys
import random

@st.cache_data
def load_data():
    """
    Loads data from a CSV file.

    Returns:
    pandas.DataFrame: The loaded data.
    """
    # data = pd.read_csv('data/csv_files/df_all_labelled.csv') 
    data = pd.read_csv('data/csv_files/schneider_processed_labelled_full.csv')
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

def data_representation_buttons(session_var, button_cols, labels):
    """
    Creates buttons for selecting data representation and updates the session state based on the selection.

    Parameters:
    session_var (str): The session state variable that stores the selected data representation.
    button_cols (list): A list of Streamlit columns for the buttons.
    labels (list): A list of labels for the buttons.

    Returns:
    None
    """
    # Initialize session state for the selection
    if session_var not in st.session_state:
        st.session_state[session_var] = labels[0]
    # Create buttons and handle selection
    for i, (button_col, label) in enumerate(zip(button_cols, labels)):
        if button_col.button(label, key=session_var+f"_{i}"):
            st.session_state[session_var] = label

def old_data_representation_buttons(session_var, button_col_freq, button_col_pct):
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

def print_choice(session_var, paths, labels, **kwargs):
    """
    Prints the graph specified by the session variable.

    Parameters:
    session_var (str): The session state variable that determines which graph to print.
    paths (list): A list of file paths of the graphs.
    labels (list): A list of labels for the buttons.
    **kwargs: Arbitrary keyword arguments for the print_graph function.

    Returns:
    None
    """
    for path, label in zip(paths, labels):
        if st.session_state[session_var] == label:
            print_graph(path, **kwargs)

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
data_comments_only = data[data['non_empty_rows']]
groupby_options = ['year', 'Zone', 'Clusters','Account Country', 'Market Segment']
# Store the parameters lists in a dictionary
my_data = {option: (np.insert(data[option].unique().astype('object'), 0, "all_time") if option == 'year' else data[option].unique()) for option in groupby_options}
# Add the merged_topics and emotions lists to the my_data dictionary
my_data['merged_topics'] = data['label'].dropna().unique()
my_data['emotions'] = data['single_emotion_label'].dropna().unique()

shorter_names={
    "single_emotion_label":"emotion",
    "sentiment_label":"sentiment",
    "Market Segment":"market",
    "Account Country":"country",
    "Zone":"zone",
    "Clusters":"cluster",
    "year":"year"
}

levels = ['Zone','Clusters','Account Country'] # it has to be from the highest level to the lowest
color_sequence = ['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A','#19D3F3','#FF6692','#B6E880','#FF97FF','#FECB52','#E763FA','#BA68C8','#FFA000','#F06292','#7986CB','#4DB6AC','#FF8A65','#A1887F','#90A4AE','#E53935','#8E24AA']


def plot_score_distribution(df, count_column, metric_type='count', **kwargs):
    if metric_type == 'count':
        # Count the frequency of each score
        score_counts = df[count_column].value_counts().sort_index()
        hover_text = ['Count: ' + str(i) for i in score_counts.values]
    elif metric_type == 'percentage':
        # Calculate the percentage of each score
        score_counts = df[count_column].value_counts(normalize=True).sort_index() * 100
        hover_text = ['Count: ' + str(j) + '<br>Percentage: ' + str(round(i, 2)) + '%' for i, j in zip(score_counts.values, df[count_column].value_counts().sort_index().values)]

    # Create a bar chart
    fig = go.Figure(data=go.Bar(x=score_counts.index, y=score_counts.values, name='', hovertext=hover_text, hoverinfo='text'))
    fig.update_layout(title='Distribution of Scores', xaxis_title='Score', yaxis_title='Frequency', **kwargs)
    
    return fig

def plots_score_distribution(df, count_column, group_column, values_list=None, metric_type="count", merge=False, **kwargs):
    # If values_list is None, get all unique values from group_column
    if values_list is None:
        values_list = df[group_column].unique()

    # Create a subplot for each unique value in the group column if not merging
    if merge:
        fig = go.Figure()
    else:
        fig = sp.make_subplots(rows=len(values_list), cols=1)

    for i, value in enumerate(values_list, start=1):
        df_group = df[df[group_column] == value]

        # Use plot_score_distribution function to create a bar chart for the group
        fig_group = plot_score_distribution(df_group, count_column, metric_type)
        
        for trace in fig_group.data:
            trace.name = str(value)  # set the trace name to the group value
            trace.hovertext = ['Group: ' + str(value) + '<br>' + text for text in trace.hovertext]
            if merge:
                fig.add_trace(trace)
            else:
                fig.add_trace(trace, row=i, col=1)

        # Add y-axis title to each subplot if not merging
        if not merge:
            fig.update_yaxes(title_text=str(value), title_standoff=0, row=i, col=1)

    # Update layout and add interactive legend
    barmode = 'group' if merge else 'stack'
    fig.update_layout(title_text=f"Distribution of {count_column} by {group_column}", barmode=barmode, showlegend=True, **kwargs)
    
    return fig

def filling_data_barchart(df, group_column, count_column, color_sequence = ['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A','#19D3F3','#FF6692','#B6E880','#FF97FF','#FECB52','#E763FA','#BA68C8','#FFA000','#F06292','#7986CB','#4DB6AC','#FF8A65','#A1887F','#90A4AE','#E53935','#8E24AA'], **kwargs):
    # Group by group_column and calculate the total number of rows and the number of rows with comments
    grouped = df.groupby(group_column).agg(
        total_rows=pd.NamedAgg(column=count_column, aggfunc='count'),
        rows_with_comments=pd.NamedAgg(column=count_column, aggfunc='sum')
    )

    # Calculate the percentage of rows with comments and without comments
    grouped['percentage_with_comments'] = round(grouped['rows_with_comments'] / grouped['total_rows'] * 100,2)
    grouped['percentage_without_comments'] = 100 - grouped['percentage_with_comments']

    # Create a color iterator
    color_iterator = cycle(color_sequence)

    # Create a stacked bar chart using go.Figure
    fig = go.Figure(data=[
        go.Bar(name=str(index), x=[index], y=[grouped.loc[index, 'percentage_with_comments']], marker_color=next(color_iterator), text='{:.1f}%'.format(grouped.loc[index, 'percentage_with_comments']), textposition='auto', hovertemplate=f'{group_column}: %{{x}}<br>Number of Comments: %{{customdata}}<extra></extra>', customdata=[grouped.loc[index, 'rows_with_comments']], showlegend=True, legendgroup=str(index)) for index in grouped.index
    ] + [
        go.Bar(name='Without Comments', x=[index], y=[grouped.loc[index, 'percentage_without_comments']], marker_color='lightgrey', hovertemplate=f'{group_column}: %{{x}}<br>Total Number of Rows: %{{customdata}}<extra></extra>', customdata=[grouped.loc[index, 'total_rows']], showlegend=False, legendgroup=str(index)) for index in grouped.index
    ])

    # Change the bar mode
    fig.update_layout(barmode='stack')

    # Set chart title and labels
    fig.update_layout(
        title_text=f'Percentage of Rows with Comments by {group_column}',
        xaxis_title=group_column,
        yaxis_title='Percentage of Rows',
        showlegend=True,
        **kwargs
    )
    
    return fig

def filling_data_barcharts(df, group_columns, count_column, values_list=None, color_sequence=['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A','#19D3F3','#FF6692','#B6E880','#FF97FF','#FECB52','#E763FA','#BA68C8','#FFA000','#F06292','#7986CB','#4DB6AC','#FF8A65','#A1887F','#90A4AE','#E53935','#8E24AA'], **kwargs):
    # If values_list is None, get all unique values from group_columns[0]
    if values_list is None:
        values_list = df[group_columns[0]].unique()

    # Filter df for only the values in values_list
    df = df[df[group_columns[0]].isin(values_list)]

    # Create a subplot for each unique value in the first group column
    fig = sp.make_subplots(rows=len(values_list), cols=1)

    for i, value in enumerate(values_list, start=1):
        df_group = df[df[group_columns[0]] == value]
        fig_group = filling_data_barchart(df_group, group_columns[1], count_column, color_sequence)

        for trace in fig_group.data:
            trace.name = trace.name.split(' - ')[0]  
            fig.add_trace(trace, row=i, col=1)              

        # Add y-axis title to each subplot
        fig.update_yaxes(title_text=str(value), title_standoff=0, row=i, col=1)

        # Only show legend for the first subplot
        if i > 1:
            for trace in fig.data[-len(fig_group.data):]:
                trace.showlegend = False

    # Update layout and add interactive legend
    fig.update_layout(
        # height=400*len(values_list), 
        title_text=f"Percentage of Rows with Comments by {group_columns[0]} and {group_columns[1]}", 
        barmode='stack', 
        showlegend=True,
        xaxis=dict(tickangle=45), # Rotate x-axis labels
        **kwargs
    )

    fig.update_xaxes(tickangle=45)

    return fig


# sunburst chart functions 
def filter_docs(df, filter_column, filter_value):
    filter_mask = df[filter_column] == filter_value
    return df[filter_mask], filter_mask

def compute_labels_and_parents(data_df, levels):
    grouped = data_df.groupby(levels).size()

    # Initialize lists
    labels = []
    parents = []

    # Compute labels and parents lists
    for i in range(len(levels)):
        for label, value in grouped.items(): # loop over the rows
            if label[i] not in labels:
                labels.append(label[i]) 
                parents.append("") if label[i] in data_df[levels[0]].values else parents.append(label[i-1])
    
    return labels, parents

def prepare_dataframe(data_df, levels):
    df_tmp=data_df.copy()
    frequency_col_name = "Count"
    df_tmp[frequency_col_name] = df_tmp.groupby(levels[-1])[levels[-1]].transform('count')
    sunburst_df = df_tmp[levels + [frequency_col_name]].drop_duplicates()
    sunburst_df[frequency_col_name] = sunburst_df[frequency_col_name].fillna(0)
    
    return sunburst_df

def compute_values(sunburst_df, labels, levels):
    values = []
    processed_labels = set()  # This set will store the labels that have been processed
    for label in labels:
        if label not in processed_labels:  # Only process the label if it has not been processed before
            for level in levels:
                if label in sunburst_df[level].values:
                    value = sunburst_df.loc[sunburst_df[level] == label, 'Count'].sum()
                    values.append(value)
                    processed_labels.add(label)  # Add the label to the set of processed labels
                    break  # No need to check other levels for this label
                    
    return values

def get_level(label, data_df, levels, return_highest_level=True): 
    # Find the levels that the label appears in
    found_levels = [level for level in levels if label in data_df[level].values]
    if not found_levels:
        # raise ValueError(f"Label {label} not found")
        return "Unknown"
    # If return_highest is True, return the first level found (highest), else return the last level found (lowest)
    if return_highest_level:
        return found_levels[0]
    else:
        return found_levels[-1]

def compute_percentages(sunburst_df, data_df, labels, parents, values, levels):
    percentages = []
    percentages_class = []
    processed_labels = set()  # This set will store the labels that have been processed
    
    for level in levels:
        # Compute total count for each label in current level
        level_counts = sunburst_df.groupby(level)['Count'].sum()

        for i, label in enumerate(labels):
            if label not in processed_labels and label in sunburst_df[level].values:
                label_count = sunburst_df.loc[sunburst_df[level] == label, 'Count'].sum() 

                # Compute total count for the parent of current label with a condition if the label has a parent or not. 
                # Without parent, the total count is the count for all labels at this highest level
                total_count = values[labels.index(parents[i])] if parents[i]!='' else level_counts.sum()
                # Compute total count from original dataframe 
                total_count_class = data_df[get_level(label, data_df, levels)].value_counts().get(label)                

                # Compute percentage for current label
                percentage = (label_count / total_count) * 100
                percentages.append(percentage)
                percentage_class = (label_count / total_count_class) * 100
                percentages_class.append(percentage_class)
                processed_labels.add(label)  # Add the label to the set of processed labels

    return percentages, percentages_class

def transform_scale_list(lst,exponent=2, desire_sum=100):
    # Apply power transformation
    transformed_lst = [i**exponent for i in lst]

    # Scale the transformed data so that the total sum remains 100
    total = sum(transformed_lst)
    scaled_lst = [(i/total)*desire_sum for i in transformed_lst]
    return scaled_lst

def normalize_percentage_class(data_df, levels, labels, parents, percentages_class, scale_exponent=2):
    # Init
    normalized_percentages_class = [0]*len(percentages_class)
    normalized_percentages_class_transform = [0]*len(percentages_class)

    ##### Highest level

    # Compute normalized_percentage_class for labels at the highest level (without parent)
    highest_level_labels = [label for label in labels if get_level(label, data_df, levels) == levels[0]]
    highest_level_indices = [labels.index(label) for label in highest_level_labels]
    total_highest_level_percentage = sum(percentages_class[i] for i in highest_level_indices)
    for i in highest_level_indices:
        normalized_percentages_class[i] = percentages_class[i] / total_highest_level_percentage * 100

    # scale the values for the highest level
    normalized_percentages_class_transform = transform_scale_list(normalized_percentages_class,scale_exponent)

    ##### Other levels

    # Normalize percentages_class based on its parent
    for level in levels[1:]: #loop on the levels except the highest one
        level_labels = [label for label in labels if get_level(label, data_df, levels) == level]
        level_indices = [labels.index(label) for label in level_labels]

        # Loop to create the normalized_percentages_class list by level
        for indice in level_indices:
            sibling_indices = [j for j, parent in enumerate(parents) if parent == parents[indice]]
            total_sibling_percentage = sum(percentages_class[j] for j in sibling_indices)
            normalized_percentage_class = percentages_class[indice] / total_sibling_percentage * normalized_percentages_class[labels.index(parents[indice])]
            normalized_percentages_class[indice] = normalized_percentage_class

        # Loop to transform the normalized_percentages_class list by level : list normalized_percentages_class_transform
        indices_updated = [] # list to avoid several treatments on each label
        for indice in level_indices:
            if indice not in indices_updated:
                sibling_indices = [j for j, parent in enumerate(parents) if parent == parents[indice]]
                # Get & Transform norm_pct_class by family (brothers with the same parent)
                norm_pct_class_sibling = [normalized_percentages_class[i] for i in sibling_indices]
                norm_pct_class_sibling_transform = transform_scale_list(norm_pct_class_sibling, scale_exponent, desire_sum=normalized_percentages_class_transform[labels.index(parents[indice])])
                # Store the transform norm_pct_class in the normalized_percentages_class_transform list
                for i, sibling_ind in enumerate(sibling_indices):
                    normalized_percentages_class_transform[sibling_ind] = norm_pct_class_sibling_transform[i]
                    indices_updated.append(sibling_ind)

    return normalized_percentages_class_transform
    
def lighten_color(color, factor):
    # Check if the input is RGB or hexadecimal
    if isinstance(color, tuple):
        r, g, b = color
    else:
        # Remove the '#' from the start of the color code if it exists
        if color.startswith('#'):
            color = color[1:]
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    # Convert RGB color to HLS
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    # Increase the lightness
    l = max(min(l + factor, 1.0), 0.0)
    # Convert back to RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    
    # Convert back to the original format
    if isinstance(color, tuple):
        return int(r*255), int(g*255), int(b*255)
    else:
        return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
    
def compute_color_list(data_df, labels, parents, levels, color_sequence):
    # Create a dictionary that maps each label to a color
    color_dict = {}

    # Sort your labels based on their level
    labels_sorted = sorted(labels, key=lambda label: get_level(label, data_df, levels), reverse=True)
    color_seq = color_sequence.copy()
    # Iterate over your reversed sorted labels list
    for i, label in enumerate(labels_sorted):
        parent = parents[labels.index(label)]  # Get the parent of the current label
        level = get_level(label, data_df, levels)  # Use your get_level function here

        if level == levels[0]:
            # Assign a unique color to each continent
            if label not in color_dict:
                # color_dict[label] = color_seq.pop(0)
                color_dict[label] = color_sequence[i % len(color_sequence)]
        else:
            # Assign a lighter shade of the parent's color to each country or city
            parent_color = color_dict[parent]
            color_dict[label] = lighten_color(parent_color, 0.1)
    return color_dict 

def add_unique_parent(labels, parents, values, unique_parent_name):
    unique_parent_value = sum(values[i] for i in range(len(parents)) if parents[i] == '')
    for i in range(len(labels)):
        if parents[i] == '':
            parents[i] = unique_parent_name
    labels.append(unique_parent_name)
    parents.append('')
    values.append(unique_parent_value)

    return labels, parents, values

def compute_lists(data_df, levels, color_sequence, class_column=None, class_value=None, unique_parent=False, unique_parent_name="Geo Levels"):
    if class_column and class_value==None:
        raise ValueError("When class_column is defined, class_value must be defined too and must be a value from the class_column column")
    
    work_df = data_df.copy()
    if class_column:
        work_df = filter_docs(data_df, class_column, class_value)[0]
    
    labels, parents = compute_labels_and_parents(work_df, levels)
    sunburst_df = prepare_dataframe(work_df, levels)
    values = compute_values(sunburst_df, labels, levels)
    # percentages, percentages_class, normalized_percentages_class = compute_percentages(sunburst_df, data_df, labels, parents, values, levels)
    percentages, percentages_class = compute_percentages(sunburst_df, data_df, labels, parents, values, levels)
    normalized_percentages_class_transform = normalize_percentage_class(data_df, levels, labels, parents, percentages_class, scale_exponent=1)
    color_dict = compute_color_list(data_df, labels, parents, levels, color_sequence)
    if unique_parent:
        labels, parents, values =  add_unique_parent(labels, parents, values, unique_parent_name=unique_parent_name)
        # Compute and add percentages for the unique_parent label
        percentages.append(100)
        percentages_class.append(len(filter_docs(data_df, class_column, class_value)[0])/len(data_df)*100) if class_column and class_value else percentages_class.append("None")
        # normalized_percentages_class.append(100) if class_column and class_value else normalized_percentages_class.append("None")
        normalized_percentages_class_transform.append(100) if class_column and class_value else normalized_percentages_class_transform.append("None")
        color_dict[unique_parent_name]='#ffffff'
    return labels, parents, values, percentages, percentages_class, normalized_percentages_class_transform, color_dict

def create_sunburst_fig(labels, parents, values, percentages, percentages_class, normalized_percentages_class_transform, color_dict, class_column=None, class_value=None, **sunburst_kwargs):
    # Create a list of hover texts that includes the percentage for each label
    hover_text = [f'{label}<br>Number of verbatims: {value}<br>Percentage: {percentage:.2f}%{f"<br>Percentage of {class_value}: {percentage_class:.2f}%" if class_column else ""}' for label, value, percentage, percentage_class in zip(labels, values, percentages, percentages_class)]

    fig = go.Figure(data=go.Sunburst(
        labels=labels,
        parents=parents,
        values=normalized_percentages_class_transform if class_column else values,
        branchvalues='total',
        hovertext=hover_text,
        hovertemplate='%{hovertext}<extra></extra>',  # Only use custom hover text and remove extra info            
        marker=dict(colors=[color_dict[label] for label in labels]),  # Set colors based on your mapping
        # insidetextorientation='radial',  # Make labels orient radially
        **sunburst_kwargs
    ))
    
    fig.update_layout(
        title={'text': f"Geographical Distribution",
               'y':0.95,'x':0.5,
               'xanchor': 'center','yanchor': 'top'},
        title_font=dict(size=20,
                        color='rgb(107, 107, 107)'),
        width=1000,
        height=1000,
    )

    return fig

def sunburst(data_df, levels, color_sequence, unique_parent=True, class_column=None, class_value=None, **sunburst_kwargs):
    labels, parents, values, percentages, percentages_class, normalized_percentages_class_transform, color_dict = compute_lists(data_df, levels, color_sequence, unique_parent=unique_parent, class_column=class_column, class_value=class_value)
    fig = create_sunburst_fig(labels, parents, values, percentages, percentages_class, normalized_percentages_class_transform, color_dict, class_column=class_column, class_value=class_value, **sunburst_kwargs)
    return fig


# Plot a bar chart or histogram of the distribution of a specified class
def plot_barchart_distribution(df, class_name, filter_col=None, filter_value=None, time_period=None, percentage_by=None, set_colors=['#96ceb4', '#87bdd8', '#ffcc5c', '#ff6f69', '#f4a688', '#d96459'], **kwargs):
    if percentage_by not in ["Topic","Class",None] :
        raise ValueError("'percentage_by' possible values are ['Topic','Class', None]")
    
    if (filter_col is None) != (filter_value is None):
        raise ValueError("Both 'filter_col' and 'filter_value' must be defined or both must be None.")
    
    work_df = df.copy()
    # Filter the data to only include rows with the specified value
    if filter_value:
        work_df = df[df[filter_col] == filter_value]

    # Filter the data by the specified time period if provided
    if time_period != None:
        if class_name == 'year':
            raise ValueError("class_name cannot be 'year' when time_period is defined")
        work_df = work_df[work_df['year'] == time_period]

    # Calculate the percentage if use_percentage is True
    if percentage_by == "Topic":
        total = len(work_df)
        filtered_data = pd.DataFrame(work_df[class_name].value_counts() / total * 100)
        filtered_data.columns = ['percentage']
        y_value = 'percentage'
    elif percentage_by == "Class":
        total_per_class = df.groupby(class_name).size()
        filtered_data = pd.DataFrame(work_df[class_name].value_counts() / total_per_class * 100)
        filtered_data.columns = ['percentage']
        y_value = 'percentage'
    else:
        filtered_data = pd.DataFrame(work_df[class_name].value_counts())
        filtered_data.columns = ['count']
        y_value = 'count'

    # Sort the data by ascending frequency if class_name is not 'year'
    if class_name != 'year':
        filtered_data.sort_values(by=y_value, ascending=True, inplace=True)
    
    # Create a color iterator
    color_sequence = set_colors
    color_iterator = cycle(color_sequence)

    fig = go.Figure(data=go.Bar(
            name=str(class_name), 
            x=filtered_data.index, 
            y=filtered_data[y_value], 
            marker_color=next(color_iterator), 
            text=[str(pd.DataFrame(work_df[class_name].value_counts()).loc[index][0]) for index in filtered_data.index],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>' + ('Count: %{customdata}<br>' + 'Percent: %{y:.2f}%' if percentage_by!=None else 'Count: %{y}<br>') + '<extra></extra>',
            customdata=[pd.DataFrame(work_df[class_name].value_counts()).loc[index] for index in filtered_data.index],
            legendgroup=str(class_name)
    ))

    # Set the axis labels
    fig.update_layout(xaxis_title=class_name, 
                      yaxis_title=y_value, 
                      title=(f'Distribution of {filter_value} by {class_name}' if filter_value else f'Distribution of {class_name}') + (f' in {time_period}' if time_period is not None else ''),
                      title_x=0.5, # Center the title
                      **kwargs
                      )

    return fig

def plot_barcharts_distribution(df, class_name, group_column, values_list=None, filter_col=None, filter_value=None, time_period=None, percentage_by=None, merge=False, color_sequence=['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A','#19D3F3','#FF6692','#B6E880','#FF97FF','#FECB52','#E763FA','#BA68C8','#FFA000','#F06292','#7986CB','#4DB6AC','#FF8A65','#A1887F','#90A4AE','#E53935','#8E24AA'], **kwargs):
    # If values_list is None, get all unique values from group_column
    if values_list is None:
        values_list = df[group_column].unique()

    # Create a subplot for each unique value in the group column if not merging
    if merge:
        fig = go.Figure()
    else:
        fig = sp.make_subplots(rows=len(values_list), cols=1)

    color_iterator = cycle(color_sequence)

    for i, value in enumerate(values_list, start=1):
        df_group = df[df[group_column] == value]

        # Use plot_score_distribution function to create a bar chart for the group
        fig_group = plot_barchart_distribution(df_group, class_name, filter_col=filter_col, filter_value=filter_value, time_period=time_period, percentage_by=percentage_by)

        for trace in fig_group.data:
            trace.name = str(value)  # set the trace name to the group value
            trace.legendgroup = trace.name
            trace.marker.color = next(color_iterator)
            trace.hovertemplate = 'Group: '+str(value)+'<br>' + ('Count: %{customdata}<br>' + 'Percentage: %{y:.2f}%<extra></extra>' if percentage_by!=None else 'Count: %{y}<br><extra></extra>')
            if merge:
                fig.add_trace(trace)
            else:
                fig.add_trace(trace, row=i, col=1)

        # Add y-axis title to each subplot if not merging
        if not merge:
            fig.update_yaxes(title_text=str(value), title_standoff=0, row=i, col=1)

    # Update layout and add interactive legend
    barmode = 'group' if merge else 'stack'
    fig.update_layout(title_text=f"Distribution of {class_name} by {group_column}", barmode=barmode, showlegend=True, **kwargs)
    
    return fig


