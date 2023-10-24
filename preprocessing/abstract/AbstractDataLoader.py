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

