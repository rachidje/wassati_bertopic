import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os
from typing import List, Union
from sklearn.preprocessing import normalize


class BertopicBarchart:
    def create_topics_per_class_df(df, bertopic_model, classes_column, filter=False, filter_group=None, filter_value=None,  sortedBy=None, ascending=True):
        """
        Create a dataframe representing the topics per class.

        This function takes as input a dataframe `df`, a BERTopic model `bertopic_model`, a column name `classes_column` representing the classes, an optional boolean parameter `filter` which determines whether to filter the data based on a subclass, an optional parameter `filter_group` representing the column name of the subclass to filter on, an optional parameter `filter_value` representing the value of the subclass to filter on, an optional parameter `sortedBy` which can be used to sort the topics by either "Frequency" or "Name", and an optional boolean parameter `ascending` which determines the sorting order (ascending or descending).

        The function first checks that the values of `sortedBy`, `ascending`, and `subclass_name` and `subclass_value` (if `filter` is `True`) are valid. If any of these values are not valid, a ValueError is raised with an appropriate error message.

        Then, depending on whether `filter` is `True` or not, the function either calculates the topics per class using the `topics_per_class` method of the BERTopic model or calls a nested function `topics_per_subclass` to compute the topics per class with filtering.

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
        if sortedBy not in [None, "Frequency", "Name"]:
            raise ValueError("sortedBy must be either None (default value), 'Frequency', or 'Name'")
        # Check that ascending is only used if sortedBy is not None
        if sortedBy is None and ascending != True:
            raise ValueError("ascending can only be used if sortedBy parameter is used")
        # Check that the value of ascending is valid
        if ascending not in [True, False]:
            raise ValueError("ascending must be either True or False")
        # Check that subclass_name and subclass_value are provided if filter is True
        if filter and (filter_group is None or filter_value is None):
            raise ValueError("If filter is True, both subclass_name and subclass_value must be provided")
        
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
            topics_per_class = topics_per_subclass()
        else:
            topics_per_class = bertopic_model.topics_per_class(df["processed_data"].astype(str).tolist(), classes=df[classes_column].to_list())

        if sortedBy=="Frequency":
            topics_per_class = topics_per_class.sort_values(by='Frequency', ascending=ascending)
        
        return topics_per_class

    def visualize_topics_per_class_options(topic_model, topics_per_class, orient="h", **kwargs):
        """
        Visualize the topic representation of major topics per class.

        This function takes as input a dataframe `df`, a topic model `topic_model`, a column name `classes_column` representing the classes, an orientation `orient` which can be either horizontal ("h") or vertical ("v"), an optional parameter `sortedBy` which can be used to sort the topics by either "Frequency" or "Name", an optional parameter `ascending` which determines the sorting order (ascending or descending), and additional keyword arguments `**kwargs`.

        The function first calculates the topics per class using the `topics_per_class` method of the topic model, which takes as input the processed data from the dataframe and the classes. Then, depending on the specified orientation and sorting options, it either uses the `visualize_topics_per_class` method of the topic model (if the orientation is horizontal) or a modified version of this method called `visualize_topics_per_class2` (if the orientation is vertical) to create a figure representing the topics per class. The figure is then returned.

        This function allows you to easily visualize the distribution of topics per class in your data using a topic model.

        Parameters:
            df (pandas.DataFrame): The input dataframe containing the data to be visualized.
            topic_model (TopicModel): The topic model used to calculate the topics per class.
            classes_column (str): The name of the column in `df` representing the classes.
            orient (str): The orientation of the visualization. Can be either "h" for horizontal or "v" for vertical. Defaults to "h".
            sortedBy (str): An optional parameter used to sort the topics by either "Frequency" or "Name". Defaults to None.
            ascending (bool): An optional parameter used to determine the sorting order. If True, sorts in ascending order. If False, sorts in descending order. Defaults to True.
            **kwargs: Additional keyword arguments passed to the visualization method.

        Returns:
            matplotlib.figure.Figure: The figure representing the topics per class.
        """
        # Modify the visualize_topics_per_class method from bertopic to be able to print a barchart vertically
        def visualize_topics_per_class_orient(topic_model,
                                    topics_per_class: pd.DataFrame,
                                    top_n_topics: int = 10,
                                    topics: List[int] = None,
                                    normalize_frequency: bool = False,
                                    custom_labels: Union[bool, str] = False,
                                    title: str = "<b>Topics per Class</b>",
                                    width: int = 1250,
                                    height: int = 900,
                                    orient: str = "h") -> go.Figure:
            """ Visualize topics per class

            Arguments:
                topic_model: A fitted BERTopic instance.
                topics_per_class: The topics you would like to be visualized with the
                                corresponding topic representation
                top_n_topics: To visualize the most frequent topics instead of all
                topics: Select which topics you would like to be visualized
                normalize_frequency: Whether to normalize each topic's frequency individually
                custom_labels: If bool, whether to use custom topic labels that were defined using 
                            `topic_model.set_topic_labels`.
                            If `str`, it uses labels from other aspects, e.g., "Aspect1".
                title: Title of the plot.
                width: The width of the figure.
                height: The height of the figure.
                orient: The orientation of the barchart, 'h' for horizontal, anything else for vertical

            Returns:
                A plotly.graph_objects.Figure including all traces

            Examples:

            To visualize the topics per class, simply run:

            ```python
            topics_per_class = topic_model.topics_per_class(docs, classes)
            topic_model.visualize_topics_per_class(topics_per_class)
            ```

            Or if you want to save the resulting figure:

            ```python
            fig = topic_model.visualize_topics_per_class(topics_per_class)
            fig.write_html("path/to/file.html")
            ```
            <iframe src="../../getting_started/visualization/topics_per_class.html"
            style="width:1400px; height: 1000px; border: 0px;""></iframe>
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
                if normalize_frequency:
                    x = normalize(trace_data.Frequency.values.reshape(1, -1))[0]
                else:
                    x = trace_data.Frequency

                ### Old part from the source github of bertopic ###
                # fig.add_trace(go.Bar(y=trace_data.Class,
                #                      x=x,
                #                      visible=visible,
                #                      marker_color=colors[index % 7],
                #                      hoverinfo="text",
                #                      name=topic_name,
                #                      orientation="h",
                #                      hovertext=[f'<b>Topic {topic}</b><br>Words: {word}' for word in words]))
                
                fig.add_trace(go.Bar(y=trace_data.Class if orient == "h" else x,
                                    x=x if orient == "h" else trace_data.Class,
                                    visible=visible,
                                    marker_color=colors[index % 7],
                                    hoverinfo="text",
                                    name=topic_name,
                                    orientation=orient,
                                    hovertext=[f'<b>Topic {topic}</b><br>Words: {word}' for word in words]))

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

        if orient=="h":
            # using the source method to do it, without having the possibility to choose the orient (at the date of 09/2023)
            # we keep the use of the source method even if we could use only the new visualize_topics_per_class_orient. Because it permits to know and enjoy the modifications done in visualize_topics_per_class in the future by the owner of this source code
            fig = topic_model.visualize_topics_per_class(topics_per_class, **kwargs)
        else:  
            # using the modified source method to do it, adding the option to print the chart vertically
            fig = visualize_topics_per_class_orient(topic_model, topics_per_class, orient=orient, **kwargs)

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
        topics_per_class = self.create_topics_per_class_df(df, bertopic_model, classes_column, filter=filter, subclass_name=filter_group, subclass_value=filter_value, sortedBy=sortedBy, ascending=ascending)
        fig = self.visualize_topics_per_class_options(bertopic_model, topics_per_class, orient=orient, **kwargs)

        return fig 
    
    def save_plotly_graph_html(plotly_fig, path, name):
        # Create the directory if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
            
        return plotly_fig.write_html(path+"/"+name+".html")

