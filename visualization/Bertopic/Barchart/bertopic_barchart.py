import pandas as pd
import plotly.graph_objects as go
from typing import List, Union
from sklearn.preprocessing import normalize
from visualization.Shared.Barchart.barchart import Barchart

class BertopicBarchart(Barchart):

    def __init__(self, bertopic_model) -> None:
        self.bertopic_model = bertopic_model

    def create_chart_per_class(self, 
                               df, 
                               classes_column, 
                               filter_value=None, 
                               sortedBy=None, 
                               ascending=True, 
                               orient="h", 
                               viz_from_source=False,
                               stacked=False, 
                               percentage_by=None,
                               **kwargs
                               ):
        """
        Create a chart representing the topics per class.

        Parameters
        ----------
            df (pandas.DataFrame): The input dataframe containing the data to be visualized.
            bertopic_model (BERTopic): The BERTopic model used to calculate the topics per class.
            classes_column (str): The name of the column in `df` representing the classes.
            filter_value: An optional parameter representing the value of the subclass to filter on. Only used if `filter` is True. Defaults to None.
            sortedBy (str): An optional parameter used to sort the topics by either "Frequency" or "Name". Defaults to None.
            ascending (bool): An optional boolean parameter used to determine the sorting order. If True, sorts in ascending order. If False, sorts in descending order. Defaults to True.
            orient (str): The orientation of the visualization. Can be either "h" for horizontal or "v" for vertical. Defaults to "h".
            **kwargs: Additional keyword arguments passed to the visualization method.

        Returns
        -------
            plotly.graph_objs.Figure: The resulting chart representing the topics per class.
        """
        topics_per_class = self.__create_topics_per_class_df(df, classes_column, filter_value=filter_value, sortedBy=sortedBy, ascending=ascending)
        self.fig = self.__visualize_topics_per_class_options(topics_per_class, orient=orient, viz_from_source=viz_from_source, stacked=stacked, percentage_by=percentage_by, **kwargs)

        return self.fig
    
    def __visualize_topics_per_class_orient(self, 
                                            bertopic_model,
                                            topics_per_class: pd.DataFrame,
                                            top_n_topics: Union[int,None] = None,
                                            topics: List[int] = None,
                                            normalize_frequency: bool = False,
                                            percentage_by: Union[str,None] = None,
                                            custom_labels: Union[bool, str] = False,
                                            title: str = "<b>Topics per Class</b>",
                                            width: int = 1250,
                                            height: int = 900,
                                            orient: str = "h", 
                                            stacked: bool = False
                                            ) -> go.Figure:
        """
        Visualizes the distribution of topics per class.

        Parameters
        ----------
            bertopic_model : The trained BERTopic model.
            topics_per_class (pd.DataFrame): A DataFrame containing the topics per class.
            top_n_topics (int, optional): The number of top topics to visualize. Defaults to 10.
            topics (List[int], optional): A list of specific topics to visualize. Defaults to None.
            normalize_frequency (bool, optional): Whether to normalize the frequency. Defaults to False.
            percentage_by (string, optional): Which percentage calcul to use for the representation of the data. Defaults to None.
            custom_labels (Union[bool, str], optional): Whether to use custom labels for the topics. Defaults to False.
            title (str, optional): The title of the plot. Defaults to "<b>Topics per Class</b>".
            width (int, optional): The width of the plot. Defaults to 1250.
            height (int, optional): The height of the plot. Defaults to 900.
            orient (str, optional): The orientation of the plot. Defaults to "h".

        Returns
        -------
            go.Figure: A Plotly figure object containing the visualization.
        """
        colors = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#D55E00", "#0072B2", "#CC79A7"]

        if percentage_by not in ["Topic","Class",None] :
            raise ValueError("'percentage_by' possible values are ['Topic','Class', None]")
    
        # Select topics based on top_n and topics args
        freq_df = bertopic_model.get_topic_freq()
        freq_df = freq_df.loc[freq_df.Topic != -1, :]
        if topics is not None:
            selected_topics = list(topics)
        elif top_n_topics is not None:
            selected_topics = sorted(freq_df.Topic.to_list()[:top_n_topics])
        else:
            selected_topics = sorted(freq_df.Topic.to_list())

        # Prepare data
        if isinstance(custom_labels, str):
            topic_names = [[[str(topic), None]] + bertopic_model.topic_aspects_[custom_labels][topic] for topic in topics]
            topic_names = ["_".join([label[0] for label in labels[:4]]) for labels in topic_names]
            topic_names = [label if len(label) < 30 else label[:27] + "..." for label in topic_names]
            topic_names = {key: topic_names[index] for index, key in enumerate(bertopic_model.topic_labels_.keys())}
        elif bertopic_model.custom_labels_ is not None and custom_labels:
            topic_names = {key: bertopic_model.custom_labels_[key + bertopic_model._outliers] for key, _ in bertopic_model.topic_labels_.items()}
        else:
            topic_names = {key: value[:40] + "..." if len(value) > 40 else value
                        for key, value in bertopic_model.topic_labels_.items()}
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

        # Check if 'percentage_by' is defined and if the corresponding percentage column exists, and use it for x values if it does
            if percentage_by is not None :
                col_name = f'{percentage_by}_Percentage'
                if col_name in trace_data.columns:
                    x = trace_data[col_name]
                else:
                    raise ValueError(f"{col_name} column does not exist")
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
                                hovertext=[f'<b>Topic {topic_names[topic]}</b><br>Words: {word}' for word in words] if percentage_by==None else [f'<b>Topic {topic_names[topic]}</b><br>Words: {word}<br>Percentage: {p}%' for word, p in zip(words, x)]
                                ))

        # Styling of the visualization
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)
        fig.update_layout(
            xaxis_title="Normalized Frequency" if normalize_frequency else "Frequency",
            yaxis_title="Class",
            barmode='stack' if stacked else "group",
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

    def __visualize_topics_per_class_options(self, 
                                             topics_per_class, 
                                             orient="h", 
                                             percentage_by=None, 
                                             viz_from_source=False, 
                                             stacked=False, 
                                             **kwargs):
        """
        Visualizes the distribution of topics per class with additional options for orientation and percentage usage.

        Parameters
        ----------
            topics_per_class : A DataFrame containing the topics per class.
            orient (str, optional): The orientation of the plot. Defaults to "h".
            use_percentage (bool, optional): Whether to use percentage for the representation of the data. Defaults to False.
            **kwargs: Arbitrary keyword arguments for the visualize_topics_per_class_orient function.

        Returns
        -------
            go.Figure: A Plotly figure object containing the visualization.
        """
        
        if viz_from_source==True and (orient!="h" or percentage_by!=None):
            raise ValueError("the option 'orient' and 'percentage_by' are not available in the visualization from bertopic source code")
        if orient=="h" and percentage_by==None and viz_from_source==True:
            # using the source method to do it, without having the possibility to choose the orient (at the date of 09/2023)
            # we keep the use of the source method even if we could use only the new visualize_topics_per_class_orient. Because it permits to know and enjoy the modifications done in visualize_topics_per_class in the future by the owner of this source code
            fig = self.bertopic_model.visualize_topics_per_class(topics_per_class, top_n_topics=None, **kwargs)
        else:  
            # using the modified source method to do it, adding the option to print the chart vertically
            fig = self.__visualize_topics_per_class_orient(self.bertopic_model, topics_per_class, orient=orient, percentage_by=percentage_by, stacked= stacked, **kwargs)

        return fig

    def __create_topics_per_class_df(self, 
                                     df, 
                                     classes_column, 
                                     filter_value=None, 
                                     sortedBy=None, 
                                     ascending=True
                                     ) -> pd.DataFrame:
        """
        Computes the distribution of topics per class in the given DataFrame. Optionally filters the data by a given subclass and sorts the resulting DataFrame.

        Parameters
        ----------
            df (pandas.DataFrame): The input DataFrame.
            classes_column (str): The name of the column in df that contains the class values.
            filter_value (str, optional): The value of the subclass to filter the data by. Required if filter is True.
            sortedBy (str, optional): Column name to sort by. Must be either None (default), 'Frequency', 'Class', 'Topic_Percentage' or 'Class_Percentage'.
            ascending (bool, optional): Whether to sort in ascending order. Default is True. Can only be used if sortedBy is not None.

        Returns
        -------
            pandas.DataFrame: A DataFrame containing the topic number, the list of words that describe the topic, and the frequency and percentage of documents from this topic that belong to each class.
        """
        # Check that the value of sortedBy is valid
        if sortedBy not in [None, "Frequency", "Class", "Topic_Percentage", "Class_Percentage"]:
            raise ValueError("sortedBy must be either None (default value), 'Frequency',  'Class', 'Topic_Percentage' or 'Class_Percentage'")
        # Check that ascending is only used if sortedBy is not None
        if sortedBy is None and ascending != True:
            raise ValueError("ascending can only be used if sortedBy parameter is used")
        # Check that the value of ascending is valid
        if ascending not in [True, False]:
            raise ValueError("ascending must be either True or False")
        
        # Compute topics_per_class dataframe using bertopic method
        topics_per_class = self.bertopic_model.topics_per_class(df["processed_data"].astype(str).tolist(), classes=df[classes_column].to_list())
        # Add percentage columns to dataframe
        topics_per_class = self.add_percentage(topics_per_class, topic_col='Topic', freq_col='Frequency')

        if filter_value : 
            # Filter your data based on the values from the chosen subclass
            topics_per_class = topics_per_class[topics_per_class['Class'] == filter_value]

            # Add rows for missing topics with a frequency of 0
            topic_words = {row['Topic']: row['Name'] for _, row in self.bertopic_model.get_topic_info().iterrows()}
            missing_topics = {topic for topic in self.bertopic_model.get_topics().keys() if topic != -1} - set(topics_per_class['Topic'].unique())
            for topic in missing_topics:
                for class_ in topics_per_class['Class'].unique():
                    new_row = pd.DataFrame({
                        'Topic': [topic],
                        'Words': [topic_words[topic]],
                        'Frequency': [0],
                        'Topic_Percentage': [0],
                        'Class_Percentage': [0],
                        'Class': [class_]
                    })
                    topics_per_class = pd.concat([topics_per_class, new_row], ignore_index=True)

        # Check if there are existing custom_labels names in the bertopic model and add them in a column if there are some
        if self.bertopic_model.custom_labels_ is not None :
            topics_per_class = self.__add_customLabelCol(topics_per_class)
        # Sort the dataframe to prepare the visualization
        if sortedBy:
            topics_per_class = topics_per_class.sort_values(by=sortedBy, ascending=ascending)
        
        return topics_per_class
    
    def __add_customLabelCol(self, df) -> pd.DataFrame:
        """
        This method adds a new column 'Name' to the input DataFrame 'df' based on the custom labels 
        from the BERTopic model 'bertopic_model'. The new column 'Name' is mapped from the 'Topic' 
        column of the DataFrame using the custom labels.

        Parameters
        ----------
            df (pandas.DataFrame): The input DataFrame to which the new column will be added.
            bertopic_model (BERTopic): The BERTopic model which contains the custom labels.

        Returns
        -------
            new_df (pandas.DataFrame): The DataFrame with the added 'Name' column.
        """
        new_df=df
        custom_labels = self.bertopic_model.custom_labels_
        custom_labels_dict = {i-1: label for i, label in enumerate(custom_labels)}
        # Add a new column 'Custom_Label' to the DataFrame
        new_df['Name'] = new_df['Topic'].map(custom_labels_dict)

        return new_df