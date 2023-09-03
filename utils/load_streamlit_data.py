from pandas import read_csv

def load_data():
    data = read_csv('data/df_all_labelled.csv')
    return data

data = load_data()