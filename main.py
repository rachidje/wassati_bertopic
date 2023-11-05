from pandas import read_csv

from utils.schneider import countries_to_update, text_data_column, words_to_filter, replacements, ngrams_list, keybert_kwargs, bertopic_kwargs, more_stopwords
from preprocessing.dataLoaders.schneider_data_loader import SchneiderDataLoader
from preprocessing.preprocessing import Preprocessor
from vocabulary.vocabulary import VocabularyCreator
from clustering.clustering import ClusteringMethod
from sklearn.feature_extraction.text import CountVectorizer

from visualization.Shared.Sunburst.sunburst_chart import SunburstChart
import nltk

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(more_stopwords)

model_name = "all-MiniLM-L6-v2"

df = read_csv("data/csv_files/schneider.csv")
schneiderDataLoader = SchneiderDataLoader(df, countries_to_update)
preprocessing = Preprocessor(
    schneiderDataLoader, 
    text_data_column,
    words_to_filter,
    replacements
)

df_full = preprocessing.preprocess()
df_preprocessed = df_full[df_full['non_empty_rows'] == True]

vocabulary_creator = VocabularyCreator(
    model_name,
    ngrams_list,
    **keybert_kwargs
)
vocabulary_list = vocabulary_creator.keybert_vocabulary(df_preprocessed)
print(len(vocabulary_list))

# On lance BERTopic avec ou sans vocabulary
clustering = ClusteringMethod(model_name)
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

# clustering.save('models/model')


### Sunburst Chart
levels = ['Zone','Clusters','Account Country'] # it has to be from the highest level to the lowest
color_sequence = ['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A','#19D3F3','#FF6692','#B6E880','#FF97FF','#FECB52','#E763FA','#BA68C8','#FFA000','#F06292','#7986CB','#4DB6AC','#FF8A65','#A1887F','#90A4AE','#E53935','#8E24AA']


sc = SunburstChart(df = read_csv('data/csv_files/df_all_labelled.csv'), levels= levels)
sc.sunburst(color_sequence= color_sequence, unique_parent= False, class_column= "single_emotion_label", class_value= "disappointment")