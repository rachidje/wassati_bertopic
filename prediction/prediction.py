import pandas as pd

class Prediction:

    def __init__(self, df, predicted_column_name, classifier, predictions) -> None:
        """
        Parameters
        ----------
            df (pd.DataFrame): The original DataFrame.
            predicted_column_name (str): The name of the column to be added to the DataFrame.
            classifier (pipeline): The Hugging Face pipeline object for making predictions.
            predictions (list): The list of predictions. Each prediction is a dictionary containing a 'label' and a 'score'.
        """
        self.df = df.copy()
        self.predicted_column_name = predicted_column_name
        self.classifier = classifier
        self.predictions = predictions

    def make_predictions_df(self) -> pd.DataFrame:
        """
        This function makes predictions on a DataFrame of documents using a given classifier. It adds the predictions to 
        the DataFrame as new columns. If the classifier is for single-label classification, it adds one column for the 
        predicted label and one for the score. If the classifier is for multi-label classification, it adds one column 
        with a dictionary of label-score pairs for each document, and two additional columns for the best label and its score.

        Returns
        -------
            pd.DataFrame: The original DataFrame with added columns for the predictions.
        """
        # Get the list of documents from the DataFrame
        docs = self.df["processed_data"].tolist()
        # Get predictions
        predictions = self.classifier(docs)
        
        # Check if predictions is a list of dictionaries (single-label case)
        if isinstance(predictions, list) and isinstance(predictions[0], dict):
            df_predicted = self.add_single_label_predictions(self.df, predictions, self.predicted_column_name)
        
        # Multi-label case
        elif isinstance(predictions, list) and isinstance(predictions[0], list):
            df_predicted = self.add_multi_label_predictions(self.df, predictions, self.predicted_column_name)

        return df_predicted
    
    def add_single_label_predictions(self) -> pd.DataFrame:
        """
        This function merges the DataFrame of single-label predictions with the original DataFrame.

        Returns
        -------
            pd.DataFrame: The original DataFrame with added columns for the predicted labels and their scores.
        """
        predicted_df = self.df
        # Convert the predictions to a DataFrame
        prediction_results = pd.DataFrame(self.predictions)
        prediction_results.rename(columns={'label': self.predicted_column_name}, inplace=True)
        # Merge the original DataFrame with the prediction results
        df_predicted = pd.concat([predicted_df, prediction_results], axis=1)
        return df_predicted

    def add_multi_label_predictions(self) -> pd.DataFrame:
        """
        This function adds a new column with multi-label predictions to the DataFrame and also adds two more columns for 
        the best label and its score.

        Returns
        -------
            pd.DataFrame: The original DataFrame with added columns for the predicted labels and their scores, as well as columns for the best label and its score.
        """
        predicted_df = self.df
        # Keep the original predictions as they are (a list of dictionaries) and add them to the DataFrame as a new column
        predicted_df[self.predicted_column_name] = self.predictions
        # Add columns for the best label and its score
        predicted_df[f'best_{self.predicted_column_name}'] = predicted_df[self.predicted_column_name].apply(lambda x: max(x.keys(), key=lambda k: x[k]) if x else None)
        predicted_df[f'best_{self.predicted_column_name}_score'] = predicted_df[self.predicted_column_name].apply(lambda x: x[max(x.keys(), key=lambda k: x[k])] if x else None)

        return predicted_df