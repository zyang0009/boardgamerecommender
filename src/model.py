import pandas as pd
import numpy as np
import pickle
import unicodedata
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

def load_data():
    with open('..data/boardgamedata.pickle', 'rb') as f:
        worddata, numdata = pickle.load(f)
    worddata.reset_index(drop=True, inplace=True)

    return worddata, numdata

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    return text

def build_model():
    pass

def save_model(prob_matrix, name='prob_matrix');
    with open(f'../models/{name}.pickle', 'wb') as f:
        pickle.dump(prob_matrix,f), name)


if __name__ == '__main__':
    pass