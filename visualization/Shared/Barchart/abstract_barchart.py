from abc import ABC, abstractmethod
import plotly.express as px
import random

class AbstractBarchart(ABC):
    @abstractmethod
    def plot_emotion(df, emotions_col_name, emotion, class_name, time_period=None, random_colors=True, set_colors=['#96ceb4', '#87bdd8', '#ffcc5c', '#ff6f69', '#f4a688', '#d96459'], set_color=None):
        """
        Plot a bar chart or histogram of the distribution of a given emotion by a specified class.

        This function takes as input a dataframe `df`, the name `emotions_col_name` of the column in df for the emotions, an emotion `emotion`, a class name `class_name` representing the column by which to group the data, an optional time period `time_period` specifying the year to filter the data by, an optional boolean parameter `random_colors` which determines whether to use a random color for the plot or a specified color, an optional list of colors `set_colors` to choose from if `random_colors` is `True`, and an optional color `set_color` to use if `random_colors` is `False`.

        The data is filtered to only include rows with the specified emotion, and further filtered by the specified time period if provided. If `random_colors` is `True`, a random color is chosen from the provided list of colors. Otherwise, the specified color is used.

        If `class_name` is not 'year', the function creates a bar chart showing the distribution of the emotion by the specified class. Otherwise, it creates a histogram showing the distribution of the emotion by year. The axis labels and title are set, and the resulting plot is returned.

        Parameters:
            df (pandas.DataFrame): The input dataframe containing the data to be plotted.
            emotions_col_name (str): The column name in df for the emotions.
            emotion (str): The emotion to be plotted.
            class_name (str): The name of the column in `df` representing the class by which to group the data.
            time_period (int): An optional integer parameter specifying the year to filter the data by. Only used if `class_name` is not 'year'. Defaults to None.
            random_colors (bool): An optional boolean parameter used to determine whether to use a random color for the plot or a specified color. Defaults to True.
            set_colors (list): An optional list of colors to choose from if `random_colors` is True. Defaults to ['#96ceb4', '#87bdd8', '#ffcc5c', '#ff6f69', '#f4a688', '#d96459'].
            set_color (str): An optional color to use if `random_colors` is False. Defaults to None.

        Returns:
            plotly.graph_objs.Figure: The resulting bar chart or histogram plot.
        """
        # Check that set_color is provided if random_colors is False
        if random_colors==False and set_color is None:
            raise ValueError("set_color must be provided if random_colors is False")
        
        # Filter the data to only include rows with the specified emotion
        filtered_data = df[df[emotions_col_name] == emotion]

        # Filter the data by the specified time period if provided
        if time_period != None:
            if class_name == 'year':
                raise ValueError("class_name cannot be 'year' when time_period is defined")
            filtered_data = filtered_data[filtered_data['year'] == time_period]

        if random_colors:
            # Randomly choose a color from the defined colors list
            colors_list = set_colors
            color = random.choice(colors_list)
        else:
            color = set_color

        # Sort the data by ascending frequency if class_name is not 'year'
        if class_name != 'year':
            filtered_data = filtered_data[class_name].value_counts(ascending=True).reset_index()
            filtered_data.columns = [class_name, 'count']
            fig = px.bar(filtered_data, x=class_name, y='count', color_discrete_sequence=[color], width=1100, height=600)
        else:
            # Create a histogram
            fig = px.histogram(filtered_data, x=class_name, nbins=20, color_discrete_sequence=[color], width=1100, height=600)

        # Set the axis labels
        fig.update_layout(xaxis_title=class_name, yaxis_title='Count')
        # Set the title
        fig.update_layout(title=f'Distribution of {emotion} by {class_name}' + (f' in {time_period}' if time_period is not None else ''))
        # Center the title
        fig.update_layout(title_x=0.5)

        return fig