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

        :param data_loader: A list of countries for which to update the translation columns.
        :type data_loader: list of str
        :param text_data_column: A list of column names to filter and/or join. Could be a unique string column name also.
        :type text_data_column: list of str, or a unique string
        :param words_to_filter: An optional list of words to filter. Defaults to None.
        :type words_to_filter: list of str, optional
        :param replacements: An optional dictionary mapping old words to new words for replacement. Defaults to None.
        :type replacements: dict, optional
        :param sep: An optional separator string to use between values when joining columns. Defaults to '. '.
        :type sep: str, optional
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

        :param df: A DataFrame of input data.
        :type df: pandas.DataFrame
        :param filter_rows: An optional boolean specifying whether or not to filter rows by removing rows where any of the specified columns contains only punctuation marks or only one or more occurrences of the specified words. Defaults to True.
        :type filter_rows: bool, optional
        :param replace_words: An optional boolean specifying whether or not to replace words in the joined column using the specified replacements. Defaults to True.
        :type replace_words: bool, optional
        :return: A modified DataFrame with additional columns, renamed columns, updated translation columns, and optionally filtered and joined rows and replaced words.
        :rtype: pandas.DataFrame
        """

        # Ensure that replacements is provided if replace_words is used
        if replace_words and not self.replacements:
            raise ValueError(
                "replacements must be provided if replace_words is used")

        # Add some additional info as columns
        ################
        self.preprocessed_df : DataFrame = self.data_loader.process()
        self.preprocessed_df['processed_data'] = self.preprocessed_df[self.text_data_column[0]].str.lower()

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

        :param df: A DataFrame to filter.
        :type df: pandas.DataFrame
        :return: A DataFrame containing only the rows where the specified column does not contain only punctuation marks or only one or more occurrences of the specified words.
        :rtype: pandas.DataFrame
        """
        # Create a regular expression pattern to match values that contain only punctuation marks or only one or more occurrences of the specified words, possibly mixed with punctuation marks
        pattern = r'^\s*[\W\s]*\s*$|^\s*(\W*\b(' + '|'.join(re.escape(word) for word in words_to_filter) + r')\b\W*)+\s*$'

        # Define a custom function to filter rows where the specified column contains only punctuation marks or only one or more occurrences of the specified words, possibly mixed with punctuation marks. It filters also the non-ASCII characters
        pattern = r'^\s*[\W\s]*\s*$|^\s*(\W*\b(' + '|'.join(re.escape(word) for word in words_to_filter) + r')\b\W*)+\s*$'
        def filter_row(row):
            for col in text_data_column:
                value = row[col]
                if notnull(value):
                    value = value.encode('ascii', 'ignore').decode('ascii')
                    if re.search(pattern, value, re.IGNORECASE):
                        return False
            return True
        
        filtered_df = df[df.apply(filter_row, axis=1)]

        return filtered_df

    @staticmethod
    def join_columns(df: DataFrame, text_data_column: List[str], sep: str):
        """
        Join the content from the specified columns in a DataFrame using a separator.

        This method takes a DataFrame as input and returns a new DataFrame where the content from the specified columns has been joined using a separator and stored in a new column.

        :param df: A DataFrame to join.
        :type df: pandas.DataFrame
        :return: A DataFrame where the content from the specified columns has been joined using a separator and stored in a new column.
        :rtype: pandas.DataFrame
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

        return df[df['processed_data'].str.len() > 0]

    @staticmethod
    def replace_words(df: DataFrame, replacements: Dict[str, str]):
        """
        Replace words in a DataFrame column using specified replacements.

        This method takes a DataFrame as input and returns a new DataFrame where words in the specified column have been replaced using the specified replacements.

        :param df: A DataFrame to replace words in.
        :type df: pandas.DataFrame
        :return: A DataFrame where words in the specified column have been replaced using the specified replacements.
        :rtype: pandas.DataFrame
        """
        series = df['processed_data']
        # Iterate over the word replacements
        for old_word, new_word in replacements.items():
            # Replace the old word with the new word in the documents using the str.replace method
            series = series.str.replace(old_word, new_word, regex=False)
        df['processed_data'] = series
        return df
