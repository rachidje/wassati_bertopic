import os
import plotly.express as px
import random
import pandas as pd

class Barchart:

    def plot_emotion(self,emotion, class_name, time_period= None, use_percentage= False, random_colors= True, set_colors= ['#96ceb4', '#87bdd8', '#ffcc5c', '#ff6f69', '#f4a688', '#d96459'], set_color= None):
        """
        This function plots a bar chart of the distribution of a specified emotion by a specified class.

        Parameters
        ----------
            emotion (str): The emotion to filter the dataframe by.
            class_name (str): The name of the class column in the dataframe.
            time_period (int, optional): The time period to filter the dataframe by. Defaults to None.
            use_percentage (bool, optional): Whether to calculate and plot percentages instead of counts. Defaults to False.
            random_colors (bool, optional): Whether to choose a color randomly from the set_colors list. If False, set_color must be provided. Defaults to True.
            set_colors (list of str, optional): The list of colors to choose from if random_colors is True. Defaults to ['#96ceb4', '#87bdd8', '#ffcc5c', '#ff6f69', '#f4a688', '#d96459'].
            set_color (str, optional): The color to use for the plot if random_colors is False. Defaults to None.

        Returns
        -------
            Figure: A Plotly figure containing the bar chart.
        """
        # Check that set_color is provided if random_colors is False
        if random_colors == False and set_color is None:
            raise ValueError("set_color must be provided if random_colors is False")
        
        # Filter the data to only include rows with the specified emotion
        filtered_data = self.df[self.df['single_emotion_label'] == emotion]

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
            total_per_zone = self.df.groupby(class_name).size()
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
    
    def add_percentage(self, df, topic_col='Topic', freq_col='Frequency', include_outliers=False):
        """
        This function adds two percentage columns to a dataframe. The first percentage is calculated as the frequency of each topic within each class. The second percentage is calculated as the frequency of each class within each topic.
        
        Parameters:
        df (DataFrame): The input dataframe.
        topic_col (str, optional): The name of the topic column in the dataframe. Defaults to 'Topic'.
        freq_col (str, optional): The name of the frequency column in the dataframe. Defaults to 'Frequency'.
        include_outliers (bool, optional): Whether to include outliers (topic number -1) in the percentage computation. Defaults to True.

        Returns:
        DataFrame: A dataframe with added 'Topic_Percentage' and 'Class_Percentage' columns.
        """ 
        # If not including outliers, remove them from the dataframe
        if not include_outliers:
            df = df[df[topic_col] != -1]

        # Check if columns exist in dataframe
        for col in [col for col in [topic_col, freq_col] if col is not None]:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataframe. The function will proceed with default column names.")

        # Calculate the total frequency per topic
        df_total_topic = df.groupby(topic_col)[freq_col].sum().reset_index()
        df_total_topic.columns = [topic_col, 'Total_Topic']

        # Calculate the total frequency per class
        df_total_class = df.groupby("Class")[freq_col].sum().reset_index()
        df_total_class.columns = ["Class", 'Total_Class']

        # Merge these two dataframes with original dataframe
        df_merged = pd.merge(df, df_total_topic, on=topic_col)
        df_merged = pd.merge(df_merged, df_total_class, on="Class")

        # Calculate the percentages and round to 2 decimal places
        df_merged['Topic_Percentage'] = (df_merged[freq_col] / df_merged['Total_Topic'] * 100).round(2)
        df_merged['Class_Percentage'] = (df_merged[freq_col] / df_merged['Total_Class'] * 100).round(2)
        
        # Replace NaN values with 0
        df_merged['Topic_Percentage'].fillna(0, inplace=True)
        df_merged['Class_Percentage'].fillna(0, inplace=True)

        # Drop the 'Total' columns
        df_merged.drop(columns=['Total_Topic', 'Total_Class'], inplace=True)

        return df_merged
    
    def save_graph_html(self, path, name):
        """
        Saves a Plotly figure as an HTML file at the specified path.

        Parameters
        ----------
            path (str): The directory where the HTML file will be saved.
            name (str): The name of the HTML file (without the .html extension).

        Returns
        -------
            None
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
            
        return self.fig.write_html(f"{path}/{name}.html")
    
