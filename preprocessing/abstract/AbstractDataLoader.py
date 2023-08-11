from abc import ABC, abstractmethod
from pandas import DataFrame, DatetimeIndex
from typing import List


class AbstractLoader(ABC):

    def __init__(self, df : DataFrame) -> None:
        self.df = df.copy()
        super().__init__()

    @abstractmethod
    def process(self) -> DataFrame:
        pass


class SchneiderDataLoader(AbstractLoader):

    def __init__(self, df: DataFrame, countries_to_update: List[str]) -> None:
        super().__init__(df)
        self.countries_to_update = countries_to_update

    def process(self) -> DataFrame:
        self.df['year'] = DatetimeIndex(self.df["Creation Date"]).year
        self.df['id'] = range(len(self.df))
        # Rename columns for readability
        self.df.rename(columns={
            'Translation to English for: Customer Comments (edited)': 'Translation_Customer_Comments',
            'Customer Comments (edited)': 'Customer_Comments',
            'Translation to English for: Overall Additional Comments (edited)': 'Translation_Overall_Additional_Comments',
            'Overall Additional Comments (edited)': 'Overall_Additional_Comments',
            'Translation to English for: Anything else comment': 'Translation_Anything_Else_Comment',
            'Anything else comment': 'Anything_Else_Comment',
            'Translation to English for: Reason for score comment': 'Translation_Reason_for_Score_Comment',
            'Reason for score comment': 'Reason_for_Score_Comment'
        }, inplace= True)
        # Create a mask to filter the rows where the 'Account Countries' column is in the list of countries to update
        mask1 = self.df['Account Country'].isin(self.countries_to_update)
        # Update the translation columns only for the rows where the mask1 is True
        mask2 = ((self.df['Customer_Comments'] != '') & self.df['Customer_Comments'].notnull()) & self.df['Translation_Customer_Comments'].isnull()
        mask = mask1 & mask2

        self.df.loc[mask, 'Translation_Customer_Comments'] = self.df.loc[mask, 'Customer_Comments']
        mask2 = ((self.df['Overall_Additional_Comments'] != '') & self.df['Overall_Additional_Comments'].notnull()) & self.df['Translation_Overall_Additional_Comments'].isnull()
        mask = mask1 & mask2

        self.df.loc[mask, 'Translation_Overall_Additional_Comments'] = self.df.loc[mask, 'Overall_Additional_Comments']
        mask2 = ((self.df['Anything_Else_Comment'] != '') & self.df['Anything_Else_Comment'].notnull()) & self.df['Translation_Anything_Else_Comment'].isnull()
        mask = mask1 & mask2

        self.df.loc[mask, 'Translation_Anything_Else_Comment'] = self.df.loc[mask, 'Anything_Else_Comment']
        mask2 = ((self.df['Reason_for_Score_Comment'] != '') & self.df['Reason_for_Score_Comment'].notnull()) & self.df['Translation_Reason_for_Score_Comment'].isnull()
        mask = mask1 & mask2

        self.df.loc[mask, 'Translation_Reason_for_Score_Comment'] = self.df.loc[mask, 'Reason_for_Score_Comment']

        return self.df
