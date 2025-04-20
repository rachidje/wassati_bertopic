from wordcloud import WordCloud
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

class WordcloudMaker:
    def get_word_freq(self, topic, top_n= 10, scale= 1, lemmatize= False) -> dict: ...

    def lemmatize_words(self, topic_words):
        """
        Lemmatize the words and combine their probabilities.

        This method takes as input a list of tuples `topic_words`, where each tuple contains a word and its probability. The function lemmatizes each word using the WordNetLemmatizer from the NLTK library, and combines the probabilities of the lemmas and their inflected forms.

        The resulting dictionary, where the keys are the lemmas and the values are their combined probabilities, is then returned.

        Parameters
        ----------
            topic_words (list): A list of tuples, where each tuple contains a word (str) and its probability (float).

        Returns
        -------
            dict: A dictionary where the keys are the lemmas (str) and the values are their combined probabilities (float).
        """
        
        get_wordnet_pos = {
            'J' : wordnet.ADJ,
            'V' : wordnet.VERB,
            'N' : wordnet.NOUN,
            'R' : wordnet.ADV
        }
        """
        Convert NLTK part of speech tags to WordNet tags.

        This function takes as input a part of speech tag in the format used by the NLTK library and returns the corresponding WordNet tag. The mapping between NLTK and WordNet tags is as follows:
        - 'J' (adjective) maps to `wordnet.ADJ`
        - 'V' (verb) maps to `wordnet.VERB`
        - 'N' (noun) maps to `wordnet.NOUN`
        - 'R' (adverb) maps to `wordnet.ADV`
        - All other tags map to `wordnet.NOUN`
        """

        # Create a lemmatizer object
        lemmatizer = WordNetLemmatizer()
        # Create a dictionary to store the lemmas and their probabilities
        lemma_prob = {}

        # Lemmatize each word and combine their probabilities
        for word, prob in topic_words:
            # Tokenize the word and get its part of speech
            tokens = nltk.word_tokenize(word)
            pos = nltk.pos_tag(tokens)[0][1]
            # Get the WordNet part of speech tag
            wordnet_pos = get_wordnet_pos[pos[0].upper()] if pos in get_wordnet_pos.keys() else wordnet.NOUN
            # Lemmatize the word
            lemma = lemmatizer.lemmatize(word, pos=wordnet_pos)
            
            # Combine the probabilities of the lemma and its inflected forms
            if lemma in lemma_prob:
                lemma_prob[lemma] += prob
            else:
                lemma_prob[lemma] = prob
        
        return lemma_prob
    
    def create_wordcloud(self, topic, top_n=10, scale=1, lemmatize=False, stopwords=None, wordcloud_kwargs=None):
        """
        Create a word cloud from a BERTopic model and a topic.

        This method takes as input a BERTopic model `topic_model`, a list of documents `docs`, a topic number `topic`, an optional integer parameter `top_n` specifying the number of words to include in the word cloud, an optional float parameter `scale` used to scale the probabilities of the words, an optional boolean parameter `lemmatize` which determines whether to lemmatize the words before creating the word cloud, an optional list of stopwords `stopwords` to be removed from the word cloud, and an optional dictionary of keyword arguments `wordcloud_kwargs` to be passed to the WordCloud constructor.

        The function first retrieves the top n words for the given topic using the `get_topic_words` function and scales their probabilities using the provided `scale` parameter. If `lemmatize` is `True`, the function lemmatizes the words using the `lemmatize_words` function and recalculates their probabilities using the `recalculate_probabilities` function. Otherwise, it uses the original words and their probabilities.

        The function then removes any stopwords from the list of words (if provided) and creates a word cloud using the WordCloud class from the wordcloud library. The resulting word cloud is then returned.

        Parameters
        ----------
            topic (int): The topic number for which to create the word cloud.
            top_n (int): An optional integer parameter specifying the number of words to include in the word cloud. Defaults to 10.
            scale (float): An optional float parameter used to scale the probabilities of the words. Defaults to 1.
            lemmatize (bool): An optional boolean parameter used to determine whether to lemmatize the words before creating the word cloud. Defaults to False.
            stopwords (list): An optional list of stopwords to be removed from the word cloud. Defaults to None.
            wordcloud_kwargs (dict): An optional dictionary of keyword arguments to be passed to the WordCloud constructor. Defaults to None.

        Returns
        -------
            wordcloud.WordCloud: The resulting word cloud.
        """
        # Get the word frequencies for a given topic.
        word_freq = self.get_word_freq(topic, top_n=top_n, scale=scale, lemmatize=lemmatize)

        # Remove stopwords from word_freq if provided
        if stopwords:
            word_freq= {word: freq for word, freq in word_freq.items() if word not in stopwords}
        
        # Create the word cloud using the words/lemmas and their probabilities
        wc = WordCloud(**(wordcloud_kwargs or {}))
        wc.generate_from_frequencies(word_freq)

        # Display the word cloud
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis("off")
        # plt.show()
        return wc