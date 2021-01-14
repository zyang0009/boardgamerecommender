import pandas as pd
import numpy as np
import pickle
import unicodedata
import re
import lxml.html
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
    try:
        df.name[df.name.str.contains(game_title)].index[0]
    except:
        return None


def find_game_id(df, idx):
    #returns game id of an array of indices of games
    return df['game.id'].iloc[idx]


def sort_by_distance(idx, probs, num_games):
    #returns array of indices of games most similiar to the provided game index
    return euclidean_distances(probs[idx].reshape(1,-1), probs).ravel().argsort()[:num_games]

def find_closest_games_names(sorted_distances, names):
    #finds names of an array of game idx's
    name_array = names.iloc[sorted_distances]
    return name_array

def find_closest_games(sorted_distances, gamedata_df):
    #finds names of an array of game idx's
    name_array = gamedata_df.iloc[sorted_distances]
    return name_array

def recommend_games(game_title, num_games):
    #returns recommendations for games in a list format
    df, numdata = load_data()
    prob_matrix = load_model()
    
    game_index = find_game_idx(df, game_title)
    if game_index == None:
        return None
    game_sim = sort_by_distance(game_index, prob_matrix, num_games+1)
    rec_df = find_closest_games(game_sim,df)
    # game_recs = find_closest_games_names(game_sim, df.name)
    # game_ids = find_game_id(df, game_recs.index)
    
    to_html = rec_df.drop(axis=1,columns='game.id')
    to_html['category'] = to_html.category.apply(lambda x: ",".join(x))
    to_html['mechanic'] = to_html.mechanic.apply(lambda x: ",".join(x))
    to_html['short_desc'] = to_html.description.apply(lambda x: ' '.join(re.split(r'(?<=[.:;])\s', x)[:4]))
    to_html['short_desc'] = to_html['short_desc'].apply(lambda x: lxml.html.fromstring(x).text_content())

    to_html.drop(axis=1,columns='description',inplace=True)
    return to_html

if __name__ == '__main__':
    pass