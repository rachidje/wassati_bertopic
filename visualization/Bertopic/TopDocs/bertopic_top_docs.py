import numpy as np

class BertopicTopDocs:

    def __init__(self, bertopic_probabilities, df, topic, top_n_docs) -> None:
        """
        Parameters
        ----------
            probabilities (numpy.ndarray): The probabilities from the BERTopic model.
            df (pandas.DataFrame): The dataframe containing the documents.
            topic (int): The topic to get the top n documents for.
            top_n_docs (int): The number of top documents to return.
        """
        self.bertopic_probabilities = bertopic_probabilities
        self.df = df.copy()
        self.topic = topic
        self.top_n_docs = top_n_docs

    def get_top_topic_docs(self):
        """
        Get the top n documents for a specified topic.
        
        Returns:
        tuple: A tuple containing a dataframe with the top n documents for the specified topic and a list with their content.
        """
        
        
        # Get the unique probabilities for the defined topic
        unique_probs = np.unique(self.bertopic_probabilities[:, self.topic])
        # Sort the unique probabilities in descending order
        sorted_unique_probs = np.sort(unique_probs)[::-1]
        
        # Initialize an empty list to store the sorted indices of all documents
        sorted_docs_indices = []
        
        # Loop over the unique probabilities
        for prob in sorted_unique_probs:
            # Sort the documents that have the current probability for the defined topic
            sorted_top_docs_indices = BertopicTopDocs.sort_docs_with_same_prob(self.bertopic_probabilities, prob, self.topic)
            # Append these indices to the list of sorted indices of all documents
            sorted_docs_indices.extend(sorted_top_docs_indices)
        
        # Take the top n from this sorted list
        final_top_docs_indices = np.array(sorted_docs_indices)[:self.top_n_docs]
        
        # Get the content of the top n documents from your dataframe
        top_docs_df = self.df.iloc[final_top_docs_indices]
        top_docs_content = top_docs_df["processed_data"].to_list()
        
        return top_docs_df, top_docs_content
    
    @staticmethod
    def sort_docs_with_same_prob(bertopic_probabilities, prob, topic):
        """
        Sort documents that have the same probability for a specified topic.

        Parameters
        ----------
            prob (float): The probability to filter by.

        Returns
        -------
            numpy.ndarray: An array containing the sorted indices of the documents that have the specified probability for the specified topic.
        """
        # Get the indices of all documents that have the current probability for the defined topic
        top_docs_indices = np.where(bertopic_probabilities[:, topic] == prob)[0]
        # Sort the probabilities for each document in descending order
        sorted_probs = -np.sort(-bertopic_probabilities[top_docs_indices], axis=1)
        # Compute the score for each document based on the difference between their first and second scores
        scores = sorted_probs[:, 0] - sorted_probs[:, 1]
        # Sort these top documents based on their scores
        sorted_top_docs_indices = top_docs_indices[np.argsort(scores)[::-1]]
        
        return sorted_top_docs_indices