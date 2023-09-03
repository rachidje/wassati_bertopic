from preprocessing.abstract.AbstractDataLoader import AbstractLoader
from pandas import DataFrame, DatetimeIndex
from typing import List

class PetitionDataLoader(AbstractLoader):

    def __init__(self, df: DataFrame)-> None:
        super().__init__(df)

    def process(self) -> DataFrame:
        self.df['year'] = DatetimeIndex(self.df["date"]).year
        self.df['id'] = range(len(self.df))
        self.df = self.df.dropna(subset= ['description'])
        self.df['title_description'] = self.df['title'] + self.df['description']
        

        return self.df