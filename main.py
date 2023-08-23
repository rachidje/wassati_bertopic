from pandas import read_csv

from utils import countries_to_update, text_data_column, words_to_filter, replacements, ngrams_list, keybert_kwargs, bertopic_kwargs, more_stopwords, labels
from preprocessing.abstract.AbstractDataLoader import SchneiderDataLoader
from preprocessing.preprocessing import Preprocessor
from vocabulary.vocabulary import VocabularyCreator
from BertTopic.clustering import ClusteringMethod
from sklearn.feature_extraction.text import CountVectorizer
import nltk

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(more_stopwords)

df = read_csv("data/schneider.csv")
schneiderDataLoader = SchneiderDataLoader(df, countries_to_update)
preprocessing = Preprocessor(
    schneiderDataLoader, 
    text_data_column,
    words_to_filter,
    replacements
)

df_preprocessed = preprocessing.preprocess()

vocabulary_creator = VocabularyCreator(
    ngrams_list,
    **keybert_kwargs
)
vocabulary_list = vocabulary_creator.keybert_vocabulary(df_preprocessed)

# On lance BERTopic avec ou sans vocabulary
clustering = ClusteringMethod()
bertopic_kwargs['vectorizer_model'] = CountVectorizer(
                    vocabulary=vocabulary_list, 
                    stop_words=stopwords, 
                    lowercase=True, 
                    ngram_range=(1, 3)
                    )


topics, probs, topic_model, embeddings = clustering.run_bertopic(
    df= df_preprocessed,
    **bertopic_kwargs
    )

clustering.save('model')