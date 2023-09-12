from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from bertopic import BERTopic
import pickle
import copy
import torch

class ClusteringMethod:

    def run_bertopic(self, df, model_name="all-MiniLM-L6-v2", **bertopic_kwargs):
        """
        Run BERTopic on a DataFrame.

        This function takes a DataFrame, an optional model name, and additional keyword arguments as input. It extracts the "processed_data" column from the DataFrame and converts it to a list of strings. Then, it extracts embeddings for the input documents using a SentenceTransformer model. Finally, it runs BERTopic on the input documents and embeddings and returns the resulting topics and probabilities.

        :param df: A DataFrame containing the input documents in the "processed_data" column.
        :param model_name: An optional string specifying the name of the SentenceTransformer model to use. Defaults to "all-MiniLM-L6-v2".
        :param bertopic_kwargs: Additional keyword arguments to be passed to the BERTopic constructor.
        :return: A tuple containing four elements: a list of topics assigned to each input document, a matrix of topic probabilities for each input document, the BERTopic model used and the embeddings.
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

    def save_bertopic_model(self, filename):
        """
        Save the BERTopic model and its associated data to a file.

        This function takes a filename as input and saves the BERTopic model and its associated data (embeddings, topics, and probabilities) to the specified file using the pickle module.

        :param filename: The name of the file to save the data to.
        """
        
        with open(filename, 'wb') as f:
            pickle.dump((self.embeddings, self.topics, self.probs, self.topic_model), f)

    def load_bertopic_model(self, filename):
        """
        Load the BERTopic model and its associated data from a file.

        This function takes a filename as input and loads the BERTopic model and its associated data (embeddings, topics, and probabilities) from the specified file using the pickle module.

        :param filename: The name of the file to load the data from.
        """

        with open(filename, 'rb') as f:
            self.embeddings, self.topics, self.probs, self.topic_model  = pickle.load(f)

    def merged_bertopic_model(docs, bertopic_model, topics_to_merge_dict, label_names_dict):
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
    
    def load_model_huggingface(model_name, task, problem_type=None, **kwargs):
        """
        This function loads a model and tokenizer from a given model name, then creates a pipeline to perform a specified task.

        Args:
            model_name (str): The name of the model to load.
            task (str): The type of task to perform with the pipeline.
            problem_type (str): The type of problem to solve ("multi_label_classification" for multi-label tasks).
            **kwargs: Additional arguments to pass to the pipeline.

        Returns:
            pipeline: A pipeline configured to perform the specified task with the loaded model and tokenizer.
        """
        model = AutoModelForSequenceClassification.from_pretrained(model_name, problem_type=problem_type)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        classifier = pipeline(task, model=model, tokenizer=tokenizer, **kwargs)
        return classifier