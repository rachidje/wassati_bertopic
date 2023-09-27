import plotly.express as px
import random
import pandas as pd

class Barchart:

    def __init__(self, df_topic_per_class) -> None:
        self.df_topic_per_class = df_topic_per_class.copy()

    def plot_emotion(self,
                     emotion, 
                     class_name, 
                     time_period= None, 
                     use_percentage= False, 
                     random_colors= True, 
                     set_colors= ['#96ceb4', '#87bdd8', '#ffcc5c', '#ff6f69', '#f4a688', '#d96459'], 
                     set_color= None):
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
    
    def topics_per_subclass(self, classes_column, bertopic_model, filter_group, filter_value) -> pd.DataFrame:
        """
        Create a dataframe that contains the topic number, the list of words that describe the topic,
        and the frequency of documents from this topic that belong to the element from the first "Class" column
        for a subset of data that is filtered by a given subclass value.
        Basically it does the same as topics_per_class method from bertopic adding a filter that depends on an other class

        Returns
        ------- 
            A pandas DataFrame containing the topic number, the list of words that describe the topic, and the frequency of documents from this topic that belong to the element from the first "Class" column for the filtered data (subclass data)
        """
        # Filter your data based on the values from the chosen subclass
        filtered_data = self.df_topic_per_class[self.df_topic_per_class[filter_group] == filter_value]
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

    def add_percentage(self, topic_col='Topic', freq_col='Frequency', class_col=None):
        """
        This function adds a percentage column to a dataframe. The percentage is calculated as the frequency of each class within each topic.
        
        Parameters
        ----------
            df (DataFrame): The input dataframe.
            topic_col (str, optional): The name of the topic column in the dataframe. Defaults to 'Topic'.
            freq_col (str, optional): The name of the frequency column in the dataframe. Defaults to 'Frequency'.
            class_col (str, optional): The name of the class column in the dataframe. If specified, the function will calculate the percentage for each class within each topic. Defaults to None.

        Returns
        -------
            DataFrame: A dataframe with an added 'Percentage' column.
        """
        # Check if columns exist in dataframe
        for col in [col for col in [topic_col, class_col, freq_col] if col is not None]:
            if col not in self.df_topic_per_class.columns:
                print(f"Warning: Column '{col}' not found in dataframe. The function will proceed with default column names.")

        # Group by 'Topic' and optionally 'Class', and sum the 'Frequency'
        group_cols = [topic_col]
        if class_col:
            group_cols.append(class_col)
        df_grouped = self.df_topic_per_class.groupby(group_cols)[freq_col].sum().reset_index()

        # Calculate the total frequency per topic
        df_total = self.df_topic_per_class.groupby(topic_col)[freq_col].sum().reset_index()
        df_total.columns = [topic_col, 'Total']

        # Merge these two dataframes
        df_merged = pd.merge(self.df_topic_per_class, df_total, on=topic_col)

        # Calculate the percentage and round to 2 decimal places
        df_merged['Percentage'] = (df_merged[freq_col] / df_merged['Total'] * 100).round(2)
        
        # Replace NaN values with 0
        df_merged['Percentage'].fillna(0, inplace=True)
        # Drop the 'Total' column
        df_merged.drop(columns=['Total'], inplace=True)

        return df_merged