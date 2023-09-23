from abc import ABC, abstractmethod
import plotly.express as px
import random
import pandas as pd

class AbstractBarchart(ABC):
    @abstractmethod
    def plot_emotion(df, emotion, class_name, time_period=None, use_percentage=False, random_colors=True, set_colors=['#96ceb4', '#87bdd8', '#ffcc5c', '#ff6f69', '#f4a688', '#d96459'], set_color=None):
        """
        This function plots a bar chart of the distribution of a specified emotion by a specified class.

        Parameters:
        df (DataFrame): The input dataframe.
        emotion (str): The emotion to filter the dataframe by.
        class_name (str): The name of the class column in the dataframe.
        time_period (int, optional): The time period to filter the dataframe by. Defaults to None.
        use_percentage (bool, optional): Whether to calculate and plot percentages instead of counts. Defaults to False.
        random_colors (bool, optional): Whether to choose a color randomly from the set_colors list. If False, set_color must be provided. Defaults to True.
        set_colors (list of str, optional): The list of colors to choose from if random_colors is True. Defaults to ['#96ceb4', '#87bdd8', '#ffcc5c', '#ff6f69', '#f4a688', '#d96459'].
        set_color (str, optional): The color to use for the plot if random_colors is False. Defaults to None.

        Returns:
        Figure: A Plotly figure containing the bar chart.
        """
        # Check that set_color is provided if random_colors is False
        if random_colors==False and set_color is None:
            raise ValueError("set_color must be provided if random_colors is False")
        
        # Filter the data to only include rows with the specified emotion
        filtered_data = df[df['single_emotion_label'] == emotion]

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

        # Calculate the percentage if use_percentage is True
        if use_percentage:
            total_per_zone = df.groupby(class_name).size()
            filtered_data = (filtered_data[class_name].value_counts() / total_per_zone * 100).reset_index()
            filtered_data.columns = [class_name, 'percentage']
            y_value = 'percentage'
        else:
            filtered_data = filtered_data[class_name].value_counts().reset_index()
            filtered_data.columns = [class_name, 'count']
            y_value = 'count'

        # Sort the data by ascending frequency if class_name is not 'year'
        if class_name != 'year':
            filtered_data.sort_values(by=y_value, ascending=True, inplace=True)

        fig = px.bar(filtered_data, x=class_name, y=y_value, color_discrete_sequence=[color], width=1100, height=600)

        # Set the axis labels
        fig.update_layout(xaxis_title=class_name, yaxis_title=y_value)
        # Set the title
        fig.update_layout(title=f'Distribution of {emotion} by {class_name}' + (f' in {time_period}' if time_period is not None else ''))
        # Center the title
        fig.update_layout(title_x=0.5)

        return fig
    
    def add_percentage(df, topic_col='Topic', freq_col='Frequency', class_col=None, group_by=None):
        """
        This function adds a percentage column to a dataframe. The percentage is calculated as the frequency of each topic within each class.
        
        Parameters:
        df (DataFrame): The input dataframe.
        topic_col (str, optional): The name of the topic column in the dataframe. Defaults to 'Topic'.
        freq_col (str, optional): The name of the frequency column in the dataframe. Defaults to 'Frequency'.
        class_col (str, optional): The name of the class column in the dataframe. If specified, the function will calculate the percentage for each topic within each class. Defaults to None.
        group_by (str, optional): Specifies whether to group by 'topic' or 'class'. Defaults to 'topic' if class_col is None, else defaults to 'class'.

        Returns:
        DataFrame: A dataframe with an added 'Percentage' column.
        
        Raises:
        ValueError: If `group_by` is not 'topic' or 'class'.
        """
        if group_by is None:
            group_by = 'Topic' if class_col is None else 'Class'
            
        if group_by not in ['Topic', 'Class']:
            raise ValueError("`group_by` should be either 'Topic' or 'Class'")
            
        # Check if columns exist in dataframe
        for col in [col for col in [topic_col, class_col, freq_col] if col is not None]:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataframe. The function will proceed with default column names.")

        # Calculate the total frequency per group
        if group_by == 'Topic' or class_col is None:
            df_total = df.groupby(topic_col)[freq_col].sum().reset_index()
        else:  # group_by == 'Class'
            df_total = df.groupby(class_col)[freq_col].sum().reset_index()
            
        df_total.columns = [group_by, 'Total']

        # Merge these two dataframes
        df_merged = pd.merge(df, df_total, on=group_by)
        # Calculate the percentage and round to 2 decimal places
        df_merged['Percentage'] = (df_merged[freq_col] / df_merged['Total'] * 100).round(2)
        
        # Replace NaN values with 0
        df_merged['Percentage'].fillna(0, inplace=True)
        # Drop the 'Total' column
        df_merged.drop(columns=['Total'], inplace=True)

        return df_merged