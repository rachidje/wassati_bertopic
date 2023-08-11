from pandas import read_csv

from utils import countries_to_update, text_data_column, words_to_filter, replacements, ngrams_list
from preprocessing.abstract.AbstractDataLoader import SchneiderDataLoader
from preprocessing.preprocessing import Preprocessor
from vocabulary.vocabulary import VocabularyCreator


df = read_csv("data/schneider.csv")
schneiderDataLoader = SchneiderDataLoader(df, countries_to_update)
preprocessing = Preprocessor(
    schneiderDataLoader, 
    text_data_column,
    words_to_filter,
    replacements
)
vocabulary_creator = VocabularyCreator(
    ngrams_list
)

df_preprocessed = preprocessing.preprocess()
df.to_csv('data/test_preprocess.csv')