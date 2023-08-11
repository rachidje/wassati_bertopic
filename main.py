from pandas import read_csv

from utils import countries_to_update, text_data_column, words_to_filter, replacements
from abstract.AbstractDataLoader import SchneiderDataLoader
from preprocessing import Preprocessor


df = read_csv("data/schneider.csv")
schneiderDataLoader = SchneiderDataLoader(df, countries_to_update)
preprocessing = Preprocessor(
    schneiderDataLoader, 
    text_data_column,
    words_to_filter,
    replacements
)

df = preprocessing.preprocess()
df.to_csv('data/test_preprocess.csv')