import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os
from typing import List, Union
from sklearn.preprocessing import normalize
from ....Shared.Barchart.abstract_barchart import add_percentage


class BertopicBarchart:
    def create_topics_per_class_df(df, bertopic_model, classes_column, filter=False, filter_group=None, filter_value=None,  sortedBy=None, ascending=True):
        """
        Create a dataframe representing the topics per class.

        This function takes as input a dataframe `df`, a BERTopic model `bertopic_model`, a column name `classes_column` representing the classes, an optional boolean parameter `filter` which determines whether to filter the data based on a subclass, an optional parameter `filter_group` representing the column name of the subclass to filter on, an optional parameter `filter_value` representing the value of the subclass to filter on, an optional parameter `sortedBy` which can be used to sort the topics by either "Frequency" or "Name", and an optional boolean parameter `ascending` which determines the sorting order (ascending or descending).

        The function first checks that the values of `sortedBy`, `ascending`, and `subclass_name` and `subclass_value` (if `filter` is `True`) are valid. If any of these values are not valid, a ValueError is raised with an appropriate error message.

        Then, depending on whether `filter` is `True` or not, the function either calculates the topics per class using the `topics_per_class` method of the BERTopic model or calls a nested function `topics_per_subclass` to compute the topics per class with filtering. It also adds a percentage column to the topics_per_class dataframe using add_percentage() method. The percentage is calculated as the frequency of each class within each topic.

        If `sortedBy` is "Frequency", the resulting dataframe is sorted by frequency in either ascending or descending order depending on the value of `ascending`.

        The resulting dataframe is then returned.

        Parameters:
            df (pandas.DataFrame): The input dataframe containing the data to be used.
            bertopic_model (BERTopic): The BERTopic model used to calculate the topics per class.
            classes_column (str): The name of the column in `df` representing the classes.
            filter (bool): An optional boolean parameter used to determine whether to filter the data based on a subclass. Defaults to False.
            filter_group (str): An optional parameter representing the column name of the subclass to filter on. Only used if `filter` is True. Defaults to None.
            filter_value: An optional parameter representing the value of the subclass to filter on. Only used if `filter` is True. Defaults to None.
            sortedBy (str): An optional parameter used to sort the topics by either "Frequency" or "Name". Defaults to None.
            ascending (bool): An optional boolean parameter used to determine the sorting order. If True, sorts in ascending order. If False, sorts in descending order. Defaults to True.

        Returns:
            pandas.DataFrame: A dataframe representing the topics per class.
        """
        
        # Check that the value of sortedBy is valid
        if sortedBy not in [None, "Frequency", "Name", "Percentage"]:
            raise ValueError("sortedBy must be either None (default value), 'Frequency',  'Name' or 'Percentage'")
        # Check that ascending is only used if sortedBy is not None
        if sortedBy is None and ascending != True:
            raise ValueError("ascending can only be used if sortedBy parameter is used")
        # Check that the value of ascending is valid
        if ascending not in [True, False]:
            raise ValueError("ascending must be either True or False")
        # Check that subclass_name and subclass_value are provided if filter is True
        if filter and (filter_group is None or filter_value is None):
            raise ValueError("If filter is True, both filter_name and filter_value must be provided")
        
        # Define a function to compute topics_per_class with filtering
        def topics_per_subclass():
            """
            Create a dataframe that contains the topic number, the list of words that describe the topic,
            and the frequency of documents from this topic that belong to the element from the first "Class" column
            for a subset of data that is filtered by a given subclass value.
            Basically it does the same as topics_per_class method from bertopic adding a filter that depends on an other class

            :param df: A pandas DataFrame containing the full data
            :param bertopic_model: A bertopic model used to compute the topics
            :param classes_column: The name of the column in df that contains the class values
            :param filter_group: The name of the column in df that contains the subclass values (the filter values)
            :param filter_value: The value of the subclass to filter the data by
            :return: A pandas DataFrame containing the topic number, the list of words that describe the topic,
                    and the frequency of documents from this topic that belong to the element from the first "Class" column
                    for the filtered data (subclass data)
            """
            # Filter your data based on the values from the chosen subclass
            filtered_data = df[df[filter_group] == filter_value]
            classes_filtered_data=filtered_data[classes_column].astype(str).tolist()
            filtered_topics = [bertopic_model.topics_[i] for i in filtered_data.index.tolist()]

            # Create manually a topic_per_class dataframe from a subset of the full documents
            topics_per_subClass_df = pd.DataFrame({'Topic': filtered_topics, 'Class': classes_filtered_data})
            # Calculate the frequency of each topic for each class
            topics_per_subClass_df = topics_per_subClass_df.groupby(['Topic', 'Class']).size().reset_index(name='Frequency')
            # Add the words that describe each topic
            topic_words = {row['Topic']: row['Name'] for _, row in bertopic_model.get_topic_info().iterrows()}
            topics_per_subClass_df['Words'] = topics_per_subClass_df['Topic'].map(topic_words)

            # Add rows for missing topics with a frequency of 0
            missing_topics = set(bertopic_model.get_topics().keys()) - set(topics_per_subClass_df['Topic'].unique())
            for topic in missing_topics:
                for class_ in topics_per_subClass_df['Class'].unique():
                    new_row = pd.DataFrame({
                        'Topic': [topic],
                        'Words': [topic_words[topic]],
                        'Frequency': [0],
                        'Class': [class_]
                    })
                    topics_per_subClass_df = pd.concat([topics_per_subClass_df, new_row], ignore_index=True)
            
            return topics_per_subClass_df

        if filter:
            topics_per_class_tmp = topics_per_subclass()
            topics_per_class = add_percentage(topics_per_class_tmp, class_col="Class")
        else:
            topics_per_class_tmp = bertopic_model.topics_per_class(df["processed_data"].astype(str).tolist(), classes=df[classes_column].to_list())
            topics_per_class = add_percentage(topics_per_class_tmp, class_col="Class")

        if sortedBy:
            topics_per_class = topics_per_class.sort_values(by=sortedBy, ascending=ascending)
 
        return topics_per_class

    def visualize_topics_per_class_options(topic_model, topics_per_class, orient="h", use_percentage=False, **kwargs):
        """
        Visualizes the distribution of topics per class with additional options for orientation and percentage usage.

        Parameters:
        topic_model : The trained BERTopic model.
        topics_per_class : A DataFrame containing the topics per class.
        orient (str, optional): The orientation of the plot. Defaults to "h".
        use_percentage (bool, optional): Whether to use percentage for the representation of the data. Defaults to False.
        **kwargs: Arbitrary keyword arguments for the visualize_topics_per_class_orient function.

        Returns:
        go.Figure: A Plotly figure object containing the visualization.
        """
        # Modify the visualize_topics_per_class method from bertopic to be able to print a barchart vertically
        def visualize_topics_per_class_orient(topic_model,
                                    topics_per_class: pd.DataFrame,
                                    top_n_topics: int = 10,
                                    topics: List[int] = None,
                                    normalize_frequency: bool = False,
                                    use_percentage: bool = False,
                                    custom_labels: Union[bool, str] = False,
                                    title: str = "<b>Topics per Class</b>",
                                    width: int = 1250,
                                    height: int = 900,
                                    orient: str = "h") -> go.Figure:
            """
            Visualizes the distribution of topics per class.

            Parameters:
            topic_model : The trained BERTopic model.
            topics_per_class (pd.DataFrame): A DataFrame containing the topics per class.
            top_n_topics (int, optional): The number of top topics to visualize. Defaults to 10.
            topics (List[int], optional): A list of specific topics to visualize. Defaults to None.
            normalize_frequency (bool, optional): Whether to normalize the frequency. Defaults to False.
            use_percentage (bool, optional): Whether to use percentage for the representation of the data. Defaults to False.
            custom_labels (Union[bool, str], optional): Whether to use custom labels for the topics. Defaults to False.
            title (str, optional): The title of the plot. Defaults to "<b>Topics per Class</b>".
            width (int, optional): The width of the plot. Defaults to 1250.
            height (int, optional): The height of the plot. Defaults to 900.
            orient (str, optional): The orientation of the plot. Defaults to "h".

            Returns:
            go.Figure: A Plotly figure object containing the visualization.
            """
            colors = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#D55E00", "#0072B2", "#CC79A7"]

            # Select topics based on top_n and topics args
            freq_df = topic_model.get_topic_freq()
            freq_df = freq_df.loc[freq_df.Topic != -1, :]
            if topics is not None:
                selected_topics = list(topics)
            elif top_n_topics is not None:
                selected_topics = sorted(freq_df.Topic.to_list()[:top_n_topics])
            else:
                selected_topics = sorted(freq_df.Topic.to_list())

            # Prepare data
            if isinstance(custom_labels, str):
                topic_names = [[[str(topic), None]] + topic_model.topic_aspects_[custom_labels][topic] for topic in topics]
                topic_names = ["_".join([label[0] for label in labels[:4]]) for labels in topic_names]
                topic_names = [label if len(label) < 30 else label[:27] + "..." for label in topic_names]
                topic_names = {key: topic_names[index] for index, key in enumerate(topic_model.topic_labels_.keys())}
            elif topic_model.custom_labels_ is not None and custom_labels:
                topic_names = {key: topic_model.custom_labels_[key + topic_model._outliers] for key, _ in topic_model.topic_labels_.items()}
            else:
                topic_names = {key: value[:40] + "..." if len(value) > 40 else value
                            for key, value in topic_model.topic_labels_.items()}
            topics_per_class["Name"] = topics_per_class.Topic.map(topic_names)
            data = topics_per_class.loc[topics_per_class.Topic.isin(selected_topics), :]

            # Add traces
            fig = go.Figure()
            for index, topic in enumerate(selected_topics):
                if index == 0:
                    visible = True
                else:
                    visible = "legendonly"
                trace_data = data.loc[data.Topic == topic, :]
                topic_name = trace_data.Name.values[0]
                words = trace_data.Words.values

            # Check if 'use_percentage' is True and 'Percentage' column exists, and use it for x values if it does
                if use_percentage :
                    if 'Percentage' in trace_data.columns:
                        x = trace_data['Percentage']
                    else:
                        raise ValueError("'Frequency' column does not exist")
                elif normalize_frequency:
                    x = normalize(trace_data.Frequency.values.reshape(1, -1))[0]
                else:
                    x = trace_data.Frequency

                fig.add_trace(go.Bar(y=trace_data.Class if orient == "h" else x,
                                    x=x if orient == "h" else trace_data.Class,
                                    visible=visible,
                                    marker_color=colors[index % 7],
                                    hoverinfo="text",
                                    name=topic_name,
                                    orientation=orient,
                                    hovertext=[f'<b>Topic {topic}</b><br>Words: {word}' for word in words] if use_percentage==False else [f'<b>Topic {topic}</b><br>Words: {word}<br>Percentage: {p}%' for word, p in zip(words, x)]
                                    ))

            # Styling of the visualization
            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)
            fig.update_layout(
                xaxis_title="Normalized Frequency" if normalize_frequency else "Frequency",
                yaxis_title="Class",
                title={
                    'text': f"{title}",
                    'y': .95,
                    'x': 0.40,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': dict(
                        size=22,
                        color="Black")
                },
                template="simple_white",
                width=width,
                height=height,
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rockwell"
                ),
                legend=dict(
                    title="<b>Global Topic Representation",
                )
            )
            return fig

        if orient=="h" and use_percentage==False:
            # using the source method to do it, without having the possibility to choose the orient (at the date of 09/2023)
            # we keep the use of the source method even if we could use only the new visualize_topics_per_class_orient. Because it permits to know and enjoy the modifications done in visualize_topics_per_class in the future by the owner of this source code
            fig = topic_model.visualize_topics_per_class(topics_per_class, **kwargs)
        else:  
            # using the modified source method to do it, adding the option to print the chart vertically
            fig = visualize_topics_per_class_orient(topic_model, topics_per_class, orient=orient, use_percentage=use_percentage, **kwargs)

        return fig

    def create_chart_per_class(
                                self,
                                df, 
                                bertopic_model, 
                                classes_column, 
                                filter=False, 
                                filter_group=None, 
                                filter_value=None, 
                                sortedBy=None, 
                                ascending=True, 
                                orient="h", 
                                **kwargs):
        """
        Create a chart representing the topics per class.

        This function takes as input a dataframe `df`, a BERTopic model `bertopic_model`, a column name `classes_column` representing the classes, an optional boolean parameter `filter` which determines whether to filter the data based on a subclass, an optional parameter `subclass_name` representing the column name of the subclass to filter on, an optional parameter `subclass_value` representing the value of the subclass to filter on, an optional parameter `sortedBy` which can be used to sort the topics by either "Frequency" or "Name", an optional boolean parameter `ascending` which determines the sorting order (ascending or descending), an orientation `orient` which can be either horizontal ("h") or vertical ("v"), and additional keyword arguments `**kwargs`.

        The function first calls the `create_topics_per_class_df` function to create a dataframe representing the topics per class. Then, it calls the `visualize_topics_per_class_options` function to create a chart from this dataframe. The resulting chart is then returned.

        Parameters:
            df (pandas.DataFrame): The input dataframe containing the data to be visualized.
            bertopic_model (BERTopic): The BERTopic model used to calculate the topics per class.
            classes_column (str): The name of the column in `df` representing the classes.
            filter (bool): An optional boolean parameter used to determine whether to filter the data based on a subclass. Defaults to False.
            filter_group (str): An optional parameter representing the column name of the subclass to filter on. Only used if `filter` is True. Defaults to None.
            filter_value: An optional parameter representing the value of the subclass to filter on. Only used if `filter` is True. Defaults to None.
            sortedBy (str): An optional parameter used to sort the topics by either "Frequency" or "Name". Defaults to None.
            ascending (bool): An optional boolean parameter used to determine the sorting order. If True, sorts in ascending order. If False, sorts in descending order. Defaults to True.
            orient (str): The orientation of the visualization. Can be either "h" for horizontal or "v" for vertical. Defaults to "h".
            **kwargs: Additional keyword arguments passed to the visualization method.

        Returns:
            plotly.graph_objs.Figure: The resulting chart representing the topics per class.
        """
        topics_per_class = self.create_topics_per_class_df(df, bertopic_model, classes_column, filter=filter, filter_name=filter_group, filter_value=filter_value, sortedBy=sortedBy, ascending=ascending)
        fig = self.visualize_topics_per_class_options(bertopic_model, topics_per_class, orient=orient, **kwargs)

        return fig 
    
    def save_plotly_graph_html(plotly_fig, path, name):
        """
        Saves a Plotly figure as an HTML file at the specified path.

        Parameters:
        fig (go.Figure): The Plotly figure to save.
        path (str): The directory where the HTML file will be saved.
        name (str): The name of the HTML file (without the .html extension).

        Returns:
        None
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
            
        return plotly_fig.write_html(path+"/"+name+".html")

