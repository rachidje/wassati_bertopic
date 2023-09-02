from pandas import DataFrame
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
import pickle

import torch

class ClusteringMethod:
    """


    """

    def run_bertopic(self, df : DataFrame, model_name : str ="all-MiniLM-L6-v2", **bertopic_kwargs):
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
        sentence_model = SentenceTransformer(model_name, device= device)
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

    def load(self, filename):
        """
        Load the BERTopic model and its associated data from a file.

        This function takes a filename as input and loads the BERTopic model and its associated data (embeddings, topics, and probabilities) from the specified file using the pickle module.

        Parameters
        ----------
            filename: str
                The name of the file to load the data from.
        Returns
        -------
            None
        """

        with open(filename, 'rb') as f:
            self.embeddings, self.topics, self.probs, self.topic_model  = pickle.load(f)
