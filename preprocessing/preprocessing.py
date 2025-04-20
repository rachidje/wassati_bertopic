import re
import string
from typing import List, Union, Dict

from pandas import DataFrame, notnull, Series
from preprocessing.abstract.AbstractDataLoader import AbstractLoader


class Preprocessor:
    """
    A class to preprocess a DataFrame of data.
    """

    def __init__(self, 
                 data_loader: AbstractLoader, 
                 text_data_column: Union[List[str], str], 
                 words_to_filter: Union[List[str], None]= None, 
                 replacements: Union[Dict[str, str], None]=None, 
                 sep: str='. '):
        """
        Initialize the preprocessor with the necessary parameters.

        Parameters
        ----------
            data_loader (List[str]): A list of countries for which to update the translation columns.
            text_data_column (List[str] | str): A list of column names to filter and/or join. Could be a unique string column name also.
            words_to_filter (List[str]): An optional list of words to filter. Defaults to None.
            replacements (Dict[str,str]): An optional dictionary mapping old words to new words for replacement. Defaults to None.
            sep (str): An optional separator string to use between values when joining columns. Defaults to '. '.
        """
        self.data_loader = data_loader
        self.text_data_column = text_data_column if isinstance(text_data_column, list) else [text_data_column]
        self.words_to_filter = words_to_filter if words_to_filter is not None else []
        self.replacements = replacements if replacements is not None else {}
        self.sep = sep

    def preprocess(self, filter_rows: bool=True, replace_words: bool=True) -> DataFrame:
        """
        Preprocess a DataFrame of data.

        This method takes a DataFrame of data and optional filter_rows, and replace_words arguments as input. It adds additional columns to the DataFrame, renames some columns for readability, updates the translation columns for specific rows, and optionally filters rows and joins columns. If replace_words is True, it also replaces words in the joined column using the specified replacements. The modified DataFrame is then returned.

        Parameters
        ----------
            df (DataFrame): A DataFrame of input data.
            filter_rows (bool): An optional boolean specifying whether or not to filter rows by removing rows where any of the specified columns contains only punctuation marks or only one or more occurrences of the specified words. Defaults to True.
            replace_words (bool): An optional boolean specifying whether or not to replace words in the joined column using the specified replacements. Defaults to True.

        Returns
        -------
            A modified DataFrame with additional columns, renamed columns, updated translation columns, and optionally filtered and joined rows and replaced words.
        """

        # Ensure that replacements is provided if replace_words is used
        if replace_words and not self.replacements:
            raise ValueError(
                "replacements must be provided if replace_words is used")

        # Add some additional info as columns
        self.preprocessed_df : DataFrame = self.data_loader.process()
        self.preprocessed_df['processed_data'] = self.preprocessed_df[self.text_data_column[0]].str.lower()

        # Initialize 'non_empty_rows' column
        self.preprocessed_df['non_empty_rows'] = True

        if filter_rows:
            self.preprocessed_df = self.filter_rows(self.preprocessed_df, self.text_data_column, self.words_to_filter)

        if len(self.text_data_column) > 1:
            self.preprocessed_df = self.join_columns(self.preprocessed_df, self.text_data_column, self.sep)

        if replace_words:
            self.preprocessed_df = self.replace_words(self.preprocessed_df, self.replacements)

        return self.preprocessed_df

    @staticmethod
    def filter_rows(df: DataFrame, text_data_column: List[str], words_to_filter: List[str]) -> DataFrame:
        """
        Filter rows from a DataFrame by removing rows where the specified column contains only punctuation marks or only one or more occurrences of the specified words.

        This method takes a DataFrame as input and returns a new DataFrame containing only the rows where the specified column does not contain only punctuation marks or only one or more occurrences of the specified words.

        Parameters
        ----------
            df: A DataFrame to filter.
            text_data_column (List[str] | str): A list of column names to filter and/or join. Could be a unique string column name also.
            words_to_filter (List[str]): An optional list of words to filter. Defaults to None.

        Returns
        -------
            A DataFrame containing only the rows where the specified column does not contain only punctuation marks or only one or more occurrences of the specified words.
        """
        new_df = df.copy()

        # Create a regular expression pattern to match values that contain only punctuation marks or only one or more occurrences of the specified words, possibly mixed with punctuation marks
        pattern = r'^\s*[\W\s]*\s*$|^\s*(\W*\b(' + '|'.join(re.escape(word) for word in words_to_filter) + r')\b\W*)+\s*$'

        # Define a custom function to filter rows where the specified column contains only punctuation marks or only one or more occurrences of the specified words, possibly mixed with punctuation marks. It filters also the non-ASCII characters
        def check_row(row):
            for col in text_data_column:
                value = row[col]
                if notnull(value):
                    value = value.encode('ascii', 'ignore').decode('ascii')
                    if re.search(pattern, value, re.IGNORECASE):
                        return False
            return True
        
        # Apply the custom function to each row and store the results in 'non_empty_rows' column
        new_df['non_empty_rows'] = new_df.apply(check_row, axis=1)

        return new_df

    @staticmethod
    def join_columns(df: DataFrame, text_data_column: List[str], sep: str):
        """
        Join the content from the specified columns in a DataFrame using a separator.

        This method takes a DataFrame as input and returns a new DataFrame where the content from the specified columns has been joined using a separator and stored in a new column.

        Parameters
        ----------
            df: A DataFrame to join.
            text_data_column (List[str] | str): A list of column names to filter and/or join. Could be a unique string column name also.
            sep (str): separator string to use between values when joining columns.

        Returns
        -------
            A DataFrame where the content from the specified columns has been joined using a separator and stored in a new column.
        """
        # Define a custom function to join the content from the specified columns using a separator
        def join_column(row):
            values = []
            for col in text_data_column:
                value = row[col]
                if notnull(value) and value.strip():
                    if values and values[-1][-1] not in string.punctuation:
                        values.append(sep)
                    else:
                        values.append(' ')
                    values.append(value)
            return ''.join(values).strip()

        # Join the content from the specified columns using the custom join_columns function
        df['processed_data'] = df.apply(join_column, axis=1)

        # Update 'non_empty_rows' for rows where 'processed_data' is an empty string
        df.loc[df['processed_data'].str.len() == 0, 'non_empty_rows'] = False

        return df

    @staticmethod
    def replace_words(df: DataFrame, replacements: Dict[str, str]) -> DataFrame:
        """
        Replace words in a DataFrame column using specified replacements.

        This method takes a DataFrame as input and returns a new DataFrame where words in the specified column have been replaced using the specified replacements.

        Parameters
        ----------
            df (DataFrame): A DataFrame to replace words in.
            replacements (Dict[str,str]): An optional dictionary mapping old words to new words for replacement. Defaults to None.
            
        Returns
        -------
        A DataFrame where words in the specified column have been replaced using the specified replacements.
        """
        series = df['processed_data']
        # Iterate over the word replacements
        for old_word, new_word in replacements.items():
            # Replace the old word with the new word in the documents using the str.replace method
            series = series.str.replace(old_word, new_word, regex=False)
        df['processed_data'] = series
        return df

    @staticmethod
    def filter_docs(df, filter_column, filter_value):
        """
        Filter a dataframe based on a specified column and value.

        Parameters
        ----------
            df (pandas.DataFrame): The dataframe to filter.
            filter_column (str): The name of the column to filter by.
            filter_value (str): The value to filter by in the specified column.

        Returns
        -------
            tuple: A tuple containing the filtered dataframe and a boolean mask indicating which rows match the specified filter.
        """
        filter_mask : Series[bool] = df[filter_column] == filter_value
        return df[filter_mask], filter_mask
    
    @staticmethod
    def convert_dict(input_dict: dict, conversion_type='keys_to_values') -> Dict[str, List[str]]:
        """
        This static method converts between a key-to-value dictionary and a value-to-keys dictionary.

        Parameters
        ----------
            input_dict (dict): The input dictionary. If conversion_type is 'keys_to_values', this should be a dictionary where the keys are the original keys and the values are the corresponding values. If conversion_type is 'values_to_keys', this should be a dictionary where the keys are the original values and the values are lists of keys for each value.
            conversion_type (str): The type of conversion to perform. Can be either 'keys_to_values' or 'values_to_keys'.

        Returns
        -------
            dict: The converted dictionary. If conversion_type is 'keys_to_values', this will be a dictionary where the keys are the original values and the values are lists of keys for each value. If conversion_type is 'values_to_keys', this will be a dictionary where the keys are the original keys and the values are the corresponding values.
        """
        if conversion_type == 'keys_to_values':
            output_dict = {}
            for key, value in input_dict.items():
                if value not in output_dict:
                    output_dict[value] = []
                output_dict[value].append(key)
        elif conversion_type == 'values_to_keys':
            output_dict = {key: value for value, keys in input_dict.items() for key in keys}
        else:
            raise ValueError("Invalid conversion_type. Must be either 'keys_to_values' or 'values_to_keys'.")
        
        return output_dict

    @staticmethod
    def add_grouping_column(df: DataFrame, key_column: str, group_dict: Dict[str, List[str]], group_column_name) -> DataFrame:
        """
        This static method adds a new column to a DataFrame with the group name of each key.

        Parameters
        ----------
            df (pd.DataFrame): The original DataFrame.
            key_column (str): The name of the column in df that contains the keys.
            group_dict (dict): A dictionary where the keys are the original keys and the values are the corresponding group names.
            group_column_name (str): The name of the new column to be added to df for the groups.

        Returns
        -------
            DataFrame: The original DataFrame with an added column for the groups.
        """
        df[group_column_name] = df[key_column].map(group_dict)
        return df