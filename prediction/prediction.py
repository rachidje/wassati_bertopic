import pandas as pd

class Prediction:

    def make_predictions_df(self, classifier, df, predicted_column_name):
        """
        This function makes predictions on a DataFrame of documents using a given classifier. It adds the predictions to 
        the DataFrame as new columns. If the classifier is for single-label classification, it adds one column for the 
        predicted label and one for the score. If the classifier is for multi-label classification, it adds one column 
        with a dictionary of label-score pairs for each document, and two additional columns for the best label and its score.

        Args:
            classifier (pipeline): The Hugging Face pipeline object for making predictions.
            df (pd.DataFrame): The DataFrame containing the documents to make predictions on. It must have a 'processed_data' 
                            column with the preprocessed text of each document.
            predicted_column_name (str): The name of the column to be added to the DataFrame for the predictions.

        Returns:
            pd.DataFrame: The original DataFrame with added columns for the predictions.
        """
        # Get the list of documents from the DataFrame
        docs = df["processed_data"].tolist()
        # Get predictions
        predictions = classifier(docs)
        
        # Check if predictions is a list of dictionaries (single-label case)
        if isinstance(predictions, list) and isinstance(predictions[0], dict):
            df_predicted = self.add_single_label_predictions(df, predictions, predicted_column_name)
        
        # Multi-label case
        elif isinstance(predictions, list) and isinstance(predictions[0], list):
            df_predicted = self.add_multi_label_predictions(df, predictions, predicted_column_name)

        return df_predicted
    
    def add_single_label_predictions(df, predictions, predicted_column_name):
        """
        This function merges the DataFrame of single-label predictions with the original DataFrame.

        Args:
            df (pd.DataFrame): The original DataFrame.
            predictions (list): The list of predictions. Each prediction is a dictionary containing a 'label' and a 'score'.
            predicted_column_name (str): The name of the column to be added to the DataFrame.

        Returns:
            pd.DataFrame: The original DataFrame with added columns for the predicted labels and their scores.
        """
        predicted_df = df
        # Convert the predictions to a DataFrame
        prediction_results = pd.DataFrame(predictions)
        prediction_results.rename(columns={'label': predicted_column_name}, inplace=True)
        # # Reset the indices of the DataFrames (if necessary)
        # df.reset_index(drop=True, inplace=True)
        # prediction_results.reset_index(drop=True, inplace=True)
        # Merge the original DataFrame with the prediction results
        df_predicted = pd.concat([predicted_df, prediction_results], axis=1)
        return df_predicted

    def add_multi_label_predictions(df, predictions, predicted_column_name):
        """
        This function adds a new column with multi-label predictions to the DataFrame and also adds two more columns for 
        the best label and its score.

        Args:
            df (pd.DataFrame): The original DataFrame.
            predictions (list): The list of predictions. Each prediction is a list of dictionaries, where each dictionary 
                                contains a 'label' and a 'score'.
            predicted_column_name (str): The name of the column to be added to the DataFrame.

        Returns:
            pd.DataFrame: The original DataFrame with added columns for the predicted labels and their scores, as well as 
                        columns for the best label and its score.
        """
        predicted_df = df
        # Keep the original predictions as they are (a list of dictionaries) and add them to the DataFrame as a new column
        predicted_df[predicted_column_name] = predictions
        # Add columns for the best label and its score
        predicted_df[f'best_{predicted_column_name}'] = predicted_df[predicted_column_name].apply(lambda x: max(x.keys(), key=lambda k: x[k]) if x else None)
        predicted_df[f'best_{predicted_column_name}_score'] = predicted_df[predicted_column_name].apply(lambda x: x[max(x.keys(), key=lambda k: x[k])] if x else None)
        return predicted_df