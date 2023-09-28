import nltk
import numpy as np

from visualization.Shared.Wordcloud.wordcloud import WordcloudMaker

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')

class BertopicWordcloud(WordcloudMaker):

    def __init__(self, bertopic_model, docs) -> None:
        """
        Constructor

        Parameters
        ----------
            bertopic_model (BERTopic): The BERTopic model used to calculate the topic words.
            docs (list): A list of documents used to fit the BERTopic model.
        """
        self.bertopic_model = bertopic_model
        self.docs = docs

    def __recalculate_probabilities(self, lemma_prob, docs):
        """
        Recalculate the c-TF-IDF scores for the lemmas.

        This function takes as input a dictionary `lemma_prob` containing the lemmas and their probabilities, a list of documents `docs`, and a BERTopic model `bertopic_model`. The function recalculates the c-TF-IDF scores for the lemmas using the provided documents and BERTopic model.

        The function first calculates the term frequencies for each lemma using the CountVectorizer from the BERTopic model. Then, it calculates the inverse document frequencies for each lemma and uses these values to compute the c-TF-IDF scores. The c-TF-IDF scores are then normalized and used to update the probabilities of the lemmas.

        The resulting dictionary, where the keys are the lemmas and the values are their updated probabilities, is then returned.

        Parameters
        ----------
            lemma_prob (dict): A dictionary where the keys are the lemmas (str) and the values are their probabilities (float).
            docs (list): A list of documents used to fit the BERTopic model.
            topic_model (BERTopic): The BERTopic model used to calculate the c-TF-IDF scores.

        Returns
        -------
            dict: A dictionary where the keys are the lemmas (str) and the values are their updated probabilities (float).
        """
        # Calculate the term frequencies using the provided CountVectorizer
        X = self.bertopic_model.vectorizer_model.transform(docs)
        
        # Calculate the term frequencies for each lemma
        tf = {}
        for lemma, prob in lemma_prob.items():
            index = self.bertopic_model.vectorizer_model.vocabulary_.get(lemma)
            if index is not None:
                tf[lemma] = np.sum(X[:, index])

        # Calculate the inverse document frequencies for each lemma
        df = np.sum(X > 0, axis=0)
        N = X.shape[0]
        idf = np.log(N / (df + 1))

        # Calculate the c-TF-IDF scores for each lemma and normalize them
        c_tf_idf = {}
        for lemma, _ in lemma_prob.items():
            index = self.bertopic_model.vectorizer_model.vocabulary_.get(lemma)
            if index is not None:
                c_tf_idf[lemma] = tf[lemma] * idf[0, index]
        c_tf_idf_sum = np.sum(list(c_tf_idf.values()))
        for lemma, score in c_tf_idf.items():
            c_tf_idf[lemma] /= c_tf_idf_sum

        # Update the probabilities of the lemmas based on their c-TF-IDF scores
        new_lemma_prob = {}
        for lemma, prob in lemma_prob.items():
            if lemma in c_tf_idf:
                new_lemma_prob[lemma] = c_tf_idf[lemma]
        
        return new_lemma_prob

    def __get_topic_words(self, topic, top_n=10):
        """
        Get the top n words for a given topic.

        This function takes as input a BERTopic model `topic_model`, a topic number `topic`, and an optional integer parameter `top_n` specifying the number of words to return. The function returns the top n words for the given topic, along with their probabilities, as a list of tuples.

        The function first retrieves the c-TF-IDF matrix and feature names from the BERTopic model. Then, it gets the row of the c-TF-IDF matrix corresponding to the given topic and uses it to find the indices of the top n words. Finally, it retrieves the words and their probabilities and returns them as a list of tuples.

        Parameters
        ----------
            topic (int): The topic number for which to retrieve the top n words.
            top_n (int): An optional integer parameter specifying the number of words to return. Defaults to 10.

        Returns
        -------
            list: A list of tuples, where each tuple contains a word (str) and its probability (float).
        """
        # Get the c-TF-IDF matrix and feature names
        c_tf_idf = self.bertopic_model.c_tf_idf_.toarray()
        feature_names = self.bertopic_model.vectorizer_model.get_feature_names_out()
        
        # Get the row of the c-TF-IDF matrix corresponding to the topic
        topic_row = c_tf_idf[topic]
        
        # Get the indices of the top_n words for the topic
        top_n_indices = np.argsort(topic_row)[::-1][:top_n]
        
        # Get the words and their probabilities
        words = [feature_names[i] for i in top_n_indices]
        probabilities = [topic_row[i] for i in top_n_indices]
        
        # Return the words and their probabilities as a list of tuples
        return list(zip(words, probabilities))

    def __group_docs_by_topic(self):
        """
        Group documents by their assigned topic.

        This function takes as input a list of documents `docs` and a BERTopic model `bertopic_model`. It creates a dictionary where the keys are topic numbers and the values are lists of documents assigned to each topic.

        Returns
        -------
            dict: A dictionary where the keys are topic numbers (int) and the values are lists of documents (list) assigned to each topic.
        """
        docs_by_topic = {}
        for doc, topic in zip(self.docs, self.bertopic_model.topics_):
            if topic+1 not in docs_by_topic:
                docs_by_topic[topic+1] = []
            docs_by_topic[topic+1].append(doc)
        
        return docs_by_topic 

    def get_word_freq(self, topic, top_n= 10, scale= 1, lemmatize= False):
        """
        Get the word frequencies for a given topic.

        This function takes as input a BERTopic model `bertopic_model`, a list of documents `docs`, a topic number `topic`, an optional integer parameter `top_n` specifying the number of words to include, an optional float parameter `scale` used to scale the probabilities of the words and an optional boolean parameter `lemmatize` which determines whether to lemmatize the words before calculating their frequencies.

        The function first retrieves the top n words for the given topic using the `get_topic_words` function and scales their probabilities using the provided `scale` parameter. If `lemmatize` is `True`, the function lemmatizes the words using the `lemmatize_words` function and recalculates their probabilities using the `recalculate_probabilities` function. Otherwise, it uses the original words and their probabilities.

        Parameters
        ----------
            topic (int): The topic number for which to calculate the word frequencies.
            top_n (int): An optional integer parameter specifying the number of words to include. Defaults to 10.
            scale (float): An optional float parameter used to scale the probabilities of the words. Defaults to 1.
            lemmatize (bool): An optional boolean parameter used to determine whether to lemmatize the words before calculating their frequencies. Defaults to False.

        Returns
        -------
            dict: A dictionary where the keys are the words/lemmas (str) and the values are their probabilities (float).
        """
        # Get the topic words and their probabilities
        topic_words = self.__get_topic_words(topic, top_n=top_n)
        # Scale the probabilities
        topic_words = [(word, prob ** scale) for word, prob in topic_words]

        if lemmatize:
            # Group documents by their assigned topic.
            docs_by_topic = self.__group_docs_by_topic()
            # get the documents assigned to a specific topic
            my_docs = docs_by_topic.get(topic, [])
            # Lemmatize the words and combine their probabilities
            lemma_prob = self.lemmatize_words(topic_words)
            # Recalculate the c-TF-IDF scores for the lemmas
            topic_words_lemma = self.__recalculate_probabilities(lemma_prob, my_docs)
            # Create a dictionary with the lemmas and their probabilities
            word_freq = {lemma: prob for lemma, prob in topic_words_lemma.items()}
        
        else:
            # Create a dictionary with the words and their probabilities
            word_freq = {word: prob for word, prob in topic_words}
        
        return word_freq 

    def create_wordclouds_bertopic(self, 
                                   top_n= 10, 
                                   scale= 1, 
                                   lemmatize= False, 
                                   stopwords= None, 
                                   wordcloud_kwargs= None, 
                                   to_save= False, 
                                   save_path= None):
        """
        Create word clouds for all topics in a BERTopic model.

        This function takes as input a BERTopic model `bertopic_model`, a list of documents `docs`, an optional integer parameter `top_n` specifying the number of words to include in each word cloud, an optional float parameter `scale` used to scale the probabilities of the words, an optional boolean parameter `lemmatize` which determines whether to lemmatize the words before creating the word clouds, an optional list of stopwords `stopwords` to be removed from the word clouds, an optional dictionary of keyword arguments `wordcloud_kwargs` to be passed to the WordCloud constructor, an optional boolean parameter `to_save` which determines whether to save the word clouds as image files, and an optional string parameter `save_path` specifying the path where the image files should be saved.

        The function first retrieves the topic information from the BERTopic model and sets the index of the resulting DataFrame to be the topic number. Then, it loops over the topic numbers in the DataFrame and calls the `create_wordcloud` function to create a word cloud for each topic. If `to_save` is `True`, it saves each word cloud as an image file at the specified location using the custom name of the topic.

        The resulting dictionary, where the keys are the custom names of the topics and the values are their corresponding word clouds, is then returned.

        Parameters
        ----------
            top_n (int): An optional integer parameter specifying the number of words to include in each word cloud. Defaults to 10.
            scale (float): An optional float parameter used to scale the probabilities of the words. Defaults to 1.
            lemmatize (bool): An optional boolean parameter used to determine whether to lemmatize the words before creating the word clouds. Defaults to False.
            stopwords (list): An optional list of stopwords to be removed from each word cloud. Defaults to None.
            wordcloud_kwargs (dict): An optional dictionary of keyword arguments to be passed to each WordCloud constructor. Defaults to None.
            to_save (bool): An optional boolean parameter used to determine whether to save each word cloud as an image file. Defaults to False.
            save_path (str): An optional string parameter specifying the path where each image file should be saved. Only used if `to_save` is True. Defaults to None.

        Returns
        -------
            dict: A dictionary where the keys are the custom names of the topics (str) and the values are their corresponding word clouds (wordcloud.WordCloud).
        """
        # Check that save_path is provided if to_save is True
        if to_save and save_path is None:
            raise ValueError("If to_save is True, save_path must be provided")
        
        # Get the topic information
        topic_info = self.bertopic_model.get_topic_info()
        # Set the index of the DataFrame to be the topic number
        topic_info = topic_info.set_index('Topic')
        wc_pics={}
        # Loop over the topic numbers in the DataFrame
        for topic_number in topic_info.index:
            # Get the custom name of the current topic for saving purpose
            topic_custom_name = topic_info.loc[topic_number, 'CustomName']
            wc_pic = self.create_wordcloud(topic_number+1, top_n=top_n, scale=scale, lemmatize=lemmatize, stopwords=stopwords, wordcloud_kwargs=wordcloud_kwargs)
            wc_pics.update({topic_custom_name: wc_pic})

            if to_save and lemmatize:
                wc_pic.to_file(f'{save_path}/{topic_custom_name}_lemmatized.png')
            elif to_save and lemmatize==False:
                wc_pic.to_file(f'{save_path}/{topic_custom_name}.png')

        return wc_pics

