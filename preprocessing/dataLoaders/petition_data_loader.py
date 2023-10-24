from preprocessing.abstract.AbstractDataLoader import AbstractLoader
from pandas import DataFrame, DatetimeIndex
from typing import List

class PetitionDataLoader(AbstractLoader):
    """
    Cette classe allows to make modifications to a DataFrame to send it to the preprocessing pipeline

    Attributes
    ----------
    df: Dataframe
        A DataFrame
    min_nb_signature : int
        The minimum number of signature a petition must have for it to be kept in the dataset

    Methods
    -------
    process():
        Launch the modifications to make
    """

    def __init__(self, df: DataFrame, min_nb_signature: int = 0)-> None:
        """
        Constructs all the necessary attributes for the petitionDataLoader object

        Parameters:
        -----------
            df: Dataframe
                A DataFrame
            min_nb_signature : int
                The minimum number of signature a petition must have for it to be kept in the dataset
        """
        super().__init__(df)
        self.min_nb_signature = min_nb_signature

    def process(self) -> DataFrame:
        """
        Apply the modifications to the DataFrame

        Parameters
        ----------
        None

        Returns
        -------
        A DataFrame modified
        """
        self.df['year'] = DatetimeIndex(self.df["date"]).year
        self.df = self.df[self.df['total_signature_count'] >= self.min_nb_signature]
        self.df = self.df.dropna(subset= ['description'])

        return self.df