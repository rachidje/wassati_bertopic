# WASSATI - NLP Analysis Project

## Overview

Our project is a comprehensive Natural Language Processing (NLP) analysis pipeline that spans from data retrieval to visualization. We leverage state-of-the-art NLP models (include BERT, BERTopic, Llama2 and others) to analyze data derived from “social network engagement”, providing valuable insights into consumer behavior and trends.

The primary aim of this project is to create a dynamic, temporal values frame of reference based on consumers-actors values. This reference base allows us to compare and align company data, providing a robust mechanism for understanding the alignment of company strategies with consumer values.

One of the key features of our project is its ability to perform advanced clustering analysis. This enables us to group similar data points together, providing a high-level overview of the data landscape. Furthermore, our system is adept at highlighting weak signals within the data, allowing us to identify subtle trends and patterns that might otherwise go unnoticed.

The results of our analysis are visualized in intuitive dashboards and our web application, making the insights accessible to both technical and non-technical stakeholders. Through these visualizations, we aim to make complex NLP analysis understandable and actionable.

In summary, our project provides a comprehensive solution for NLP analysis, from data retrieval to insightful visualizations. Whether you’re interested in understanding consumer values, aligning company strategies, or identifying weak signals in your data, our project offers the tools and insights you need.

Technically the data is retrieved, preprocessed and then fed into our NLP pipeline. This pipeline includes steps for tokenization, lemmatization, named entity recognition, keywords extraction or sentiment analysis. The results are then clustered using our custom clustering algorithm based on BERTopic or our custom NMF solution to identify common themes and trends.

The entire ML and NLP system is implemented in Python and makes use of several popular libraries and frameworks, including pandas, nltk, sklearn, spacy, hugging face transformers, and others.

## Installation

This project uses conda for managing dependencies and environments. Follow these steps to set up the project:

Clone the repository: Clone this repository to your local machine.
git clone https://github.com/yourusername/yourproject.git

if a environment.yml is provided (conda way):

Create a conda environment: Navigate to the project directory and create a conda environment using the provided environment.yml file. This will install all necessary dependencies.
cd yourproject
conda env create -f environment.yml

Activate the environment: Activate the newly created conda environment.
conda activate your_environment_name

if a requirements.txt is provided (pip way):

Create a new conda environment (replace myenv with the name you want to give to your environment):
conda create --name myenv python=3.9

Activate the newly created environment:
conda activate myenv

Install pip in the new environment:
conda install pip

Navigate to the directory with your requirements.txt file and install the dependencies using pip:
cd /path/to/your/project
pip install -r requirements.txt


Run the project: You’re now ready to run the project! See the Usage section for more details.

## Usage

Explain here how to use the main.py file, its parameters 

## Directory Structure

Here’s a high-level overview of our project’s directory structure:

.
├── main.py  # Main script that runs the entire pipeline
├── models  # Contains pre-trained models
│   ├── raw_keybert_bertopic_model
│   └── raw_keybert_bertopic_model_data.pkl
├── notebooks  # Jupyter notebooks for exploratory data analysis and prototyping
│   ├── schneider_0shot.ipynb
│   ├── schneider_clustering_final.ipynb
│   └── schneider_clustering_final_old.ipynb
├── prediction  # Scripts for making predictions with the trained models
│   └── prediction.py
├── preprocessing  # Scripts for preprocessing the data
│   ├── abstract
│   │   └── AbstractDataLoader.py
│   └── preprocessing.py
├── streamlit_app.py  # Streamlit application for interactive data exploration and visualization
├── utils.py  # Utility functions used across the project
├── visualization  # Scripts for visualizing the data and results
│   ├── Bertopic
│   │   ├── Barchart
│   │   │   └── bertopic_barchart.py
│   │   ├── TopDocs
│   │   │   └── bertopic_top_docs.py
│   │   └── Wordcloud
│   │       └── bertopic_wordcloud.py
│   └── Shared  # Shared visualization scripts used across different parts of the project
│       ├── Barchart
│       │   └── barchart.py
│       └── Wordcloud
│           └── wordcloud.py
└── vocabulary  # Scripts for creating and managing the data's vocabulary
    └── vocabulary.py

## Data Flow diagram

1. Start
2. Data Retrieval (this part is not present in this project)
3. Preprocessing: Clean and preprocess the data for analysis.
4. Vocabulary (optional): Create a specific vocabulary to our data to feed our model with.
5. Clustering: Analyze the data grouping similar data points together.
6. Prediction: Add the results from the clustering/classification method into our original data
7. Visualization: Visualize the results in dashboards and web application.
    - Barchart : Create barchart figures.
    - Wordcloud : Create wordcloud images.
    - TopDocs : Retrieve the best documents according to a specific filter.
8. End


