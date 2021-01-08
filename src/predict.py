import pandas as pd
import numpy as np
import pickle
import unicodedata
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances

def load_data():
    with open('../data/boardgamedata.pickle', 'rb') as f:
        worddata, numdata = pickle.load(f)
    worddata.reset_index(drop=True, inplace=True)

    return worddata, numdata

def load_model():
    with open('../models/prob_matrix.pickle', 'rb') as f:
        game_probs = pickle.load(f)
    return game_probs

def find_game_idx(df, game_title):
    #returns the first found index of a game given a name search string query
    return df.name[df.name.str.contains(game_title)].index[0]


def find_game_id(df, idx):
    #returns game id of an array of indices of games
    return df['game.id'].iloc[idx]


def sort_by_distance(idx, probs, distance_funct=cosine_distances, num_games=10):
    #returns array of indices of games most similiar to the provided game index
    return euclidean_distances(probs[idx].reshape(1,-1), probs).ravel().argsort()[:10]

def find_closest_games_names(sorted_distances, names):
    #finds names of an array of game idx's
    name_array = names.iloc[sorted_distances]
    return name_array

def recommend_games(game_title, num_games):
    #returns recommendations for games in a list format
    df, numdata = load_data()
    prob_matrix = load_model()
    
    game_index = find_game_idx(df, game_title)
    game_sim = sort_by_distance(game_index, prob_matrix, num_games)
    game_recs = find_closest_games_names(game_sim, df.name)
    game_ids = find_game_id(df, game_recs.index)
    
    rec_df = pd.DataFrame({'id':game_ids,'name':game_recs})
    
    return list(rec_df.name)

if __name__ == '__main__':
    print(recommend_games('Catan',10))