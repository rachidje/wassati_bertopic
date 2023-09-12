from abc import ABC, abstractmethod
from wordcloud import WordCloud

class AbstractWordcloud(ABC):
    @abstractmethod
    def create_wordcloud(word_freq_dict, stopwords=None, wordcloud_kwargs=None):
        """
        Creates a word cloud from a dictionary of word frequencies.

        Parameters:
        word_freq_dict (dict): A dictionary where keys are words and values are their frequencies.
        stopwords (list, optional): A list of words to be removed from the word_freq_dict. Defaults to None.
        wordcloud_kwargs (dict, optional): A dictionary of arguments to be passed to the WordCloud constructor. Defaults to None.

        Returns:
        WordCloud: A WordCloud object.
        """
        # Remove stopwords from word_freq_dict if provided
        if stopwords:
            word_freq = {word: freq for word, freq in word_freq_dict.items() if word not in stopwords}
        
        # Create the word cloud using the words and their probabilities
        wc = WordCloud(**(wordcloud_kwargs or {}))
        wc.generate_from_frequencies(word_freq)

        return wc
    
