import copy
from pandas import DataFrame
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
import pickle

import torch

class ClusteringMethod:
    
    def __init__(self, model_name) -> None:
        self.model_name = model_name

    def run_bertopic(self, df : DataFrame, **bertopic_kwargs):
        """
        Run BERTopic on a DataFrame.

        This function takes a DataFrame, an optional model name, and additional keyword arguments as input. It extracts the "processed_data" column from the DataFrame and converts it to a list of strings. Then, it extracts embeddings for the input documents using a SentenceTransformer model. Finally, it runs BERTopic on the input documents and embeddings and returns the resulting topics and probabilities.

        Parameters
        ----------
            df: DataFrame
                A DataFrame containing the input documents in the "processed_data" column.
            model_name: str
                An optional string specifying the name of the SentenceTransformer model to use. Defaults to "all-MiniLM-L6-v2".
            bertopic_kwargs: dict
                Additional keyword arguments to be passed to the BERTopic constructor.

        Returns
        -------
            A tuple containing four elements: a list of topics assigned to each input document, a matrix of topic probabilities for each input document, the BERTopic model used and the embeddings.
        """

        # Extract documents from DataFrame
        docs = df["processed_data"].astype(str).tolist()

        # Extract embeddings
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        sentence_model = SentenceTransformer(self.model_name, device= device)
        self.embeddings = sentence_model.encode(docs, show_progress_bar=True)

        # Run BERTopic
        self.topic_model = BERTopic(embedding_model=sentence_model, **bertopic_kwargs)
        self.topics, self.probs = self.topic_model.fit_transform(docs, self.embeddings)

        # Store data

        return self.topics, self.probs, self.topic_model, self.embeddings

    def save(self, filename):
        """
        Save the BERTopic model and its associated data to a file.

        This function takes a filename as input and saves the BERTopic model and its associated data (embeddings, topics, and probabilities) to the specified file using the pickle module.

        Parameters
        ----------
            filename: str
                The name of the file to save the data to.

        Returns
        -------
            None
        """
        
        with open(filename, 'wb') as f:
            pickle.dump((self.embeddings, self.topics, self.probs, self.topic_model), f)

    @staticmethod
    def load_bertopic_model(filename):
        """
        Load a BERTopic model and associated data from a file.
        
        :param filename: The name of the file to load the data from.
        :return: A tuple containing the loaded BERTopic model, topics, probs, and docs variables.
        """
        # Load the BERTopic model
        topic_model = BERTopic.load(filename)
        
        # Load the topics, probs, and docs variables
        with open(filename + '_data.pkl', 'rb') as f:
            topics, probs, embeddings, docs = pickle.load(f)
        
        return topic_model, topics, probs, embeddings, docs
    
    @staticmethod
    def create_merged_model(docs, bertopic_model, topics_to_merge_dict, label_names_dict):
        """
        Create a new BERTopic model by merging topics from an existing model.

        This function takes as input a list of documents `docs`, an existing BERTopic model `bertopic_model`, a dictionary `topics_to_merge_dict` specifying which topics to merge, and a dictionary `label_names_dict` specifying the labels for the merged topics.

        The function creates a deep copy of the input BERTopic model and merges the specified topics using the `merge_topics` method. Then, it sets the topic labels for the merged model using the `set_topic_labels` method and the provided `label_names_dict`.

        The resulting merged BERTopic model is then returned.

        Parameters:
            docs (list): A list of documents used to fit the BERTopic model.
            bertopic_model (BERTopic): The input BERTopic model to be merged.
            topics_to_merge_dict (dict): A dictionary specifying which topics to merge. The keys are the topic numbers to be merged, and the values are the topic numbers into which they should be merged.
            label_names_dict (dict): A dictionary specifying the labels for the merged topics. The keys are the topic numbers, and the values are the corresponding labels.

        Returns:
            BERTopic: The resulting merged BERTopic model.
        """
        topic_model_merged = copy.deepcopy(bertopic_model)
        topic_model_merged.merge_topics(docs, topics_to_merge_dict)

        # Create a dictionary to match the aggregated name to their corresponding topic number
        mergedtopic_labels_dict = {i-1: item for i, item in enumerate(label_names_dict)}
        # Set topic labels for the aggregated model
        topic_model_merged.set_topic_labels(mergedtopic_labels_dict)

        return topic_model_merged
