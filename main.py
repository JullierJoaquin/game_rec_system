import fastapi
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

import ast
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


vectorizer = TfidfVectorizer()
app = fastapi.FastAPI()


model_data = pd.read_csv("data/model_data.csv", index_col=0, parse_dates=["date"])

@app.get("/")
def test():
    return {"API STEAM GAMES ACTIVE"}


@app.get("/{title}")
def recommend_similar_games(title):

    # Encuentra el índice del juego ingresado
    game_index = model_data[model_data['title'] == title].index[0]

    # Filtra los juegos basados en la fecha de lanzamiento
    year = model_data["date"].dt.year[game_index]
    five_years_ago = year - 5
    five_years_later = year + 5
    filtered_data = model_data[(model_data["date"].dt.year >= five_years_ago) & (model_data["date"].dt.year <= five_years_later)]

    # Filtra los juegos basados price category
    price = model_data["price_discr"][game_index]
    upper_price = price + 1
    lower_price = price - 1
    filtered_data = filtered_data[(filtered_data["price_discr"] >= lower_price) & (filtered_data["price_discr"] <= upper_price)]
    
    filtered_data = filtered_data.reset_index(drop=True)
    new_game_index = filtered_data[filtered_data['title'] == title].index[0]

    # Create similarity matrix based on popular genres for filtered_data
    popular_genres_matrix = vectorizer.fit_transform(filtered_data['popular_genres'])
    popular_genres_similarity_matrix = cosine_similarity(popular_genres_matrix, popular_genres_matrix)
    # Create similarity matrix based on common genres for filtered_data
    common_genres_matrix = vectorizer.fit_transform(filtered_data['common_genres'])
    common_genres_similarity_matrix = cosine_similarity(common_genres_matrix, common_genres_matrix)
    # Create similarity matrix based on unpopular genres for filtered_data
    unpopular_genres_matrix = vectorizer.fit_transform(filtered_data['unpopular_genres'])
    unpopular_genres_similarity_matrix = cosine_similarity(unpopular_genres_matrix, unpopular_genres_matrix)
    # Combine the similarity matrices for the three genre categories
    similarity_matrix = popular_genres_similarity_matrix + common_genres_similarity_matrix + unpopular_genres_similarity_matrix

    
    # Adjust the game indices for the filtered_data
    similar_game_indices = similarity_matrix[new_game_index].argsort()[::-1][1:6]

    # Obtain the names of similar games and their similarity scores
    similar_game_scores = similarity_matrix[game_index][similar_game_indices]
    similar_game_titles = filtered_data.iloc[similar_game_indices]['title'].tolist()

    # Create a DataFrame with titles and similarity scores
    similar_games_dict = {'combined_score': similar_game_scores.tolist(), 'title': similar_game_titles}

    return similar_games_dict


def test():
    return {"API STEAM GAMES ACTIVE"}