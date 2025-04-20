from pandas import DataFrame
import plotly.graph_objects as go
import colorsys

from bertopic import BERTopic
from typing import List, Union
from sklearn.preprocessing import normalize

class SunburstChart:

    def __init__(self,df: DataFrame, levels: List[str]) -> None:
        self.levels = levels
        self.data_df = df.copy()

    def __filter_docs(self, filter_column: str, filter_value: Union[str, None]):
        filter_mask = self.data_df[filter_column] == filter_value

        return self.data_df[filter_mask], filter_mask

    def __compute_labels_and_parents(self, data_df: DataFrame):
        grouped = data_df.groupby(self.levels).size()

        # Initialize lists
        labels = []
        parents = []

        # Compute labels and parents lists
        for i in range(len(self.levels)):
            for label, _ in grouped.items(): # loop over the rows
                if label[i] not in labels:
                    labels.append(label[i]) 
                    parents.append("") if label[i] in data_df[self.levels[0]].values else parents.append(label[i-1])
        
        return labels, parents

    def __prepare_dataframe(self, data_df: DataFrame):
        df_tmp=data_df.copy()
        frequency_col_name = "Count"
        df_tmp[frequency_col_name] = df_tmp.groupby(self.levels[-1])[self.levels[-1]].transform('count')
        sunburst_df = df_tmp[self.levels + [frequency_col_name]].drop_duplicates()
        sunburst_df[frequency_col_name] = sunburst_df[frequency_col_name].fillna(0)
        
        return sunburst_df

    def __compute_values(self, sunburst_df: DataFrame, labels):
        values = []
        processed_labels = set()  # This set will store the labels that have been processed
        for label in labels:
            if label not in processed_labels:  # Only process the label if it has not been processed before
                for level in self.levels:
                    if label in sunburst_df[level].values:
                        value = sunburst_df.loc[sunburst_df[level] == label, 'Count'].sum()
                        values.append(value)
                        processed_labels.add(label)  # Add the label to the set of processed labels
                        break  # No need to check other levels for this label
                        
        return values

    def __get_level(self, label: str, return_highest_level: bool =True): 
        # Find the levels that the label appears in
        found_levels = [level for level in self.levels if label in self.data_df[level].values]
        if not found_levels:
            # raise ValueError(f"Label {label} not found")
            return "Unknown"
        # If return_highest is True, return the first level found (highest), else return the last level found (lowest)
        if return_highest_level:
            return found_levels[0]
        else:
            return found_levels[-1]

    def __compute_percentages(self, sunburst_df: DataFrame, labels: List[str], parents, values):
        percentages = []
        percentages_class = []
        processed_labels = set()  # This set will store the labels that have been processed
        
        for level in self.levels:
            # Compute total count for each label in current level
            level_counts = sunburst_df.groupby(level)['Count'].sum()

            for i, label in enumerate(labels):
                if label not in processed_labels and label in sunburst_df[level].values:
                    label_count = sunburst_df.loc[sunburst_df[level] == label, 'Count'].sum() 

                    # Compute total count for the parent of current label with a condition if the label has a parent or not. 
                    # Without parent, the total count is the count for all labels at this highest level
                    total_count = values[labels.index(parents[i])] if parents[i]!='' else level_counts.sum()
                    # Compute total count from original dataframe 
                    total_count_class = self.data_df[self.__get_level(label)].value_counts().get(label)

                    # Compute percentage for current label
                    percentage = (label_count / total_count) * 100
                    percentages.append(percentage)
                    percentage_class = (label_count / total_count_class) * 100
                    percentages_class.append(percentage_class)
                    processed_labels.add(label)  # Add the label to the set of processed labels

        return percentages, percentages_class

    def __transform_scale_list(self, lst,exponent: int = 2, desire_sum: int = 100):
        # Apply power transformation
        transformed_lst = [i**exponent for i in lst]

        # Scale the transformed data so that the total sum remains 100
        total = sum(transformed_lst)
        scaled_lst = [(i/total)*desire_sum for i in transformed_lst]
        return scaled_lst

    def __normalize_percentage_class(self, labels, parents, percentages_class, scale_exponent=2):
        # Init
        normalized_percentages_class = [0]*len(percentages_class)
        normalized_percentages_class_transform = [0]*len(percentages_class)

        ##### Highest level

        # Compute normalized_percentage_class for labels at the highest level (without parent)
        highest_level_labels = [label for label in labels if self.__get_level(label) == self.levels[0]]
        highest_level_indices = [labels.index(label) for label in highest_level_labels]
        total_highest_level_percentage = sum(percentages_class[i] for i in highest_level_indices)
        for i in highest_level_indices:
            normalized_percentages_class[i] = percentages_class[i] / total_highest_level_percentage * 100

        # scale the values for the highest level
        normalized_percentages_class_transform = self.__transform_scale_list(normalized_percentages_class,scale_exponent)

        ##### Other levels

        # Normalize percentages_class based on its parent
        for level in self.levels[1:]: #loop on the levels except the highest one
            level_labels = [label for label in labels if self.__get_level(label) == level]
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
                    norm_pct_class_sibling_transform = self.__transform_scale_list(norm_pct_class_sibling, scale_exponent, desire_sum=normalized_percentages_class_transform[labels.index(parents[indice])])
                    # Store the transform norm_pct_class in the normalized_percentages_class_transform list
                    for i, sibling_ind in enumerate(sibling_indices):
                        normalized_percentages_class_transform[sibling_ind] = norm_pct_class_sibling_transform[i]
                        indices_updated.append(sibling_ind)

        return normalized_percentages_class_transform
        
    def __lighten_color(self, color, factor):
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
        
    def __compute_color_list(self, labels, parents, color_sequence):
        # Create a dictionary that maps each label to a color
        color_dict = {}

        # Sort your labels based on their level
        labels_sorted = sorted(labels, key=lambda label: self.__get_level(label), reverse=True)
        color_seq = color_sequence.copy()
        # Iterate over your reversed sorted labels list
        for i, label in enumerate(labels_sorted):
            parent = parents[labels.index(label)]  # Get the parent of the current label
            level = self.__get_level(label)  # Use your get_level function here

            if level == self.levels[0]:
                # Assign a unique color to each continent
                if label not in color_dict:
                    # color_dict[label] = color_seq.pop(0)
                    color_dict[label] = color_sequence[i % len(color_sequence)]
            else:
                # Assign a lighter shade of the parent's color to each country or city
                parent_color = color_dict[parent]
                color_dict[label] = self.__lighten_color(parent_color, 0.1)
        return color_dict 

    def __add_unique_parent(self, labels, parents, values, unique_parent_name):
        unique_parent_value = sum(values[i] for i in range(len(parents)) if parents[i] == '')
        for i in range(len(labels)):
            if parents[i] == '':
                parents[i] = unique_parent_name
        labels.append(unique_parent_name)
        parents.append('')
        values.append(unique_parent_value)

        return labels, parents, values

    def __compute_lists(self, color_sequence, class_column=None, class_value: Union[str, None] =None, unique_parent=False, unique_parent_name="Geo Levels"):
        if class_column and class_value==None:
            raise ValueError("When class_column is defined, class_value must be defined too and must be a value from the class_column column")
        
        work_df = self.data_df.copy()
        if class_column:
            work_df = self.__filter_docs(class_column, class_value)[0]
        
        labels, parents = self.__compute_labels_and_parents(work_df)
        sunburst_df = self.__prepare_dataframe(work_df)
        values = self.__compute_values(sunburst_df, labels)


        percentages, percentages_class = self.__compute_percentages(sunburst_df, labels, parents, values)
        normalized_percentages_class_transform = self.__normalize_percentage_class(labels, parents, percentages_class, scale_exponent=1)
        color_dict = self.__compute_color_list(labels, parents, color_sequence)

        if unique_parent:
            labels, parents, values =  self.__add_unique_parent(labels, parents, values, unique_parent_name=unique_parent_name)
            # Compute and add percentages for the unique_parent label
            percentages.append(100)
            percentages_class.append(len(self.__filter_docs(class_column, class_value)[0])/len(self.data_df)*100) if class_column and class_value else percentages_class.append("None")
            # normalized_percentages_class.append(100) if class_column and class_value else normalized_percentages_class.append("None")
            normalized_percentages_class_transform.append(100) if class_column and class_value else normalized_percentages_class_transform.append("None")
            color_dict[unique_parent_name]='#ffffff'

        return labels, parents, values, percentages, percentages_class, normalized_percentages_class_transform, color_dict

    def __create_sunburst_fig(self, labels, parents, values, percentages, percentages_class, normalized_percentages_class_transform, color_dict, class_column=None, class_value=None, **sunburst_kwargs):
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
            **sunburst_kwargs
        ))
        
        fig.update_layout(
            title={'text': f"Geographical Distribution",
                'y':0.95,'x':0.5,
                'xanchor': 'center','yanchor': 'top'},
            title_font=dict(size=20,
                            color='rgb(107, 107, 107)'),
            width=1100,
            height=1000
        )

        return fig

    def sunburst(self, color_sequence, unique_parent=True, class_column=None, class_value=None, **sunburst_kwargs):
        labels, parents, values, percentages, percentages_class, normalized_percentages_class_transform, color_dict = \
            self.__compute_lists(color_sequence, unique_parent=unique_parent, class_column=class_column, class_value=class_value)
        
        fig = self.__create_sunburst_fig(labels, parents, values, percentages, percentages_class, normalized_percentages_class_transform, color_dict, class_column=class_column, class_value=class_value, **sunburst_kwargs)
        return fig