from typing import Union, List
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
import torch


class VocabularyCreator:
    """
    A class to create a custom vocabulary from a list of documents using KeyBERT.
    """
    def __init__(self, ngrams_list: Union[List[str], None] = None, model_name: str ="all-MiniLM-L6-v2", **keybert_kwargs):
        """
        Initialize the vocabulary creator with the necessary parameters.

        :param ngrams_list: An optional list of custom n-grams to be replaced with single tokens during preprocessing. Defaults to None.
        :type ngrams_list: list of str, optional
        :param model_name: An optional string specifying the name of the SentenceTransformer model to use. Defaults to "all-MiniLM-L6-v2".
        :type model_name: str, optional
        :param keybert_kwargs: Additional keyword arguments to be passed to the KeyBERT `extract_keywords` method.        
        """
        self.ngrams_list = ngrams_list if ngrams_list is not None else []
        self.model_name = model_name
        self.keybert_kwargs = keybert_kwargs

    def keybert_vocabulary(self, df):
        """
        Create a custom vocabulary from a DataFrame using KeyBERT.

        This method takes a DataFrame as input. If ngrams_list is not empty, it preprocesses the documents by replacing the custom n-grams with single tokens containing underscores. Then, it initializes a GPU-enabled SentenceTransformer model and uses KeyBERT to extract keywords from the preprocessed documents. If ngrams_list is not empty, the extracted keywords are postprocessed by replacing single tokens with the original n-grams and removing duplicates to create the custom vocabulary. The vocabulary is returned as a list of strings.

        :param df: A DataFrame of input data.
        :type df: pandas.DataFrame
        :return: A list of strings representing the custom vocabulary created from the input dataframe.
        :rtype: list of str
        """

        preprocessed_df = df.copy()

        # Preprocess documents by replacing custom n-grams with single tokens containing underscores
        if self.ngrams_list:
            preprocessed_df = self.underscore_ngrams(preprocessed_df)

        # Extract the list of documents from the 'processed_data' column
        docs = preprocessed_df["processed_data"].astype(str).tolist()

        # Initialize a GPU-enabled SentenceTransformer model
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = SentenceTransformer(self.model_name, device=device)

        # Extract keywords using KeyBERT
        kw_model = KeyBERT(model=model)
        keywords = kw_model.extract_keywords(docs, **self.keybert_kwargs)
        
        # Flatten the list of lists and remove duplicates to create the vocabulary
        vocabulary = list(set([word for sublist in keywords for word, _ in sublist]))

        # Postprocess extracted keywords by replacing single tokens with original n-grams
        if self.ngrams_list:
            postprocessed_vocab = self.restore_ngrams(vocabulary)
        else:
            postprocessed_vocab = vocabulary

        return postprocessed_vocab

    def underscore_ngrams(self, df):
        """
        Replace spaces with underscores in n-grams in a DataFrame.

        This method takes a DataFrame of data as input, replaces spaces with underscores in n-grams in the 'processed_data' column, and returns a modified DataFrame as output.

        :param df: A DataFrame to preprocess.
        :type df: pandas.DataFrame
        :return: A DataFrame where the 'processed_data' column has been preprocessed.
        :rtype: pandas.DataFrame
        """

        preprocessed_df = df.copy()
        
        # Perform preprocessing steps on the 'processed_data' column
        underscore_ngrams_list = list(map(lambda x : x.replace(" ", "_"), self.ngrams_list))
        ngram_replacements = dict(zip(self.ngrams_list, underscore_ngrams_list))
        preprocessed_df['processed_data'] = preprocessed_df['processed_data'].replace(ngram_replacements, regex=True)
        
        return preprocessed_df

    def restore_ngrams(self, vocabulary):
        """
        Replace underscores with spaces in n-grams in a list of extracted keywords.

        This method takes a list of extracted keywords as input and returns a new list of postprocessed keywords where each single token containing underscores has been replaced with the original n-gram.

        :param vocabulary: A list of extracted keywords, where each keyword is a string.
        :type vocabulary: list of str
        :return: A list of postprocessed keywords where each single token containing underscores has been replaced with the original n-gram.
        :rtype: list of str
        """

        postprocessed_vocab = []
        for keyword in vocabulary:
            space_keyword = keyword.replace("_"," ")
            if space_keyword in self.ngrams_list:
                keyword = space_keyword
            postprocessed_vocab.append(keyword)
        return postprocessed_vocab
