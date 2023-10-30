import ast
import fastapi
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
app = fastapi.FastAPI()

steam_games = pd.read_csv("data/steam_games.csv", index_col=0, parse_dates=["date"])
steam_games["genres"] = steam_games["genres"].fillna("[]")
steam_games['genres'] = steam_games['genres'].apply(eval)

users_items = pq.read_table('data/users_items.parquet')
users_items = users_items.to_pandas()
users_reviews = pq.read_table('data/users_reviews.parquet')
users_reviews = users_reviews.to_pandas()

model_data = pd.read_csv("data/model_data.csv", index_col=0, parse_dates=["date"])
model_data['popular_genres'].fillna('', inplace=True)
model_data['common_genres'].fillna('', inplace=True)
model_data['unpopular_genres'].fillna('', inplace=True)

@app.get("/")
def test():
    return {"API STEAM GAMES ACTIVE"}


@app.get("/developer/{developer}")
def developer(developer):

    developer_data = steam_games[steam_games["developer"] == developer]

    game_count_by_year = developer_data["date"].dt.year.value_counts()
    game_count_by_year_df = pd.DataFrame(game_count_by_year).reset_index()
    game_count_by_year_df.columns = ["year", "item_count"]

    free_game_count_by_year = developer_data["date"][developer_data["price"] == 0].dt.year.value_counts()
    free_game_count_by_year_df = pd.DataFrame(free_game_count_by_year).reset_index()
    free_game_count_by_year_df.columns = ["year", "free_item_count"]

    game_count_by_year_df = pd.merge(game_count_by_year_df, free_game_count_by_year_df, on="year", how="left")    
    game_count_by_year_df["free_content"] = game_count_by_year_df["free_item_count"] * 100 / game_count_by_year_df["item_count"]
    game_count_by_year_df.drop(columns="free_item_count", inplace=True)

    result_dict = game_count_by_year_df.to_dict(orient="records")
    return result_dict


@app.get("/userdata/{user_id}")
def userdata(user_id: str):

    user_items = users_items[users_items["user_id"] == user_id ]
    user_reviews = users_reviews[users_reviews["user_id"] == user_id]

    user_items = user_items.merge(steam_games[["game_id", "price"]], on="game_id", how="left")    
    spent_money = user_items["price"].sum()

    item_count = user_reviews.shape[0]
    recommend_rate = user_reviews["recommend"].value_counts()[True] * 100 / item_count
    
    user_data = {"user_id": user_id, "spent_money": spent_money, "recommend_rate": recommend_rate, "item_count": item_count}

    return user_data


@app.get("/userforgenre/{genre}")
def UserForGenre(genre: str):

    genre_items = users_items.merge(steam_games[["genres", "game_id", "date"]], on="game_id", how="left")
    genre_items["genres"] = genre_items["genres"].fillna("[]")
    genre_items = genre_items[genre_items["genres"].apply(lambda x: genre in x)]

    data = genre_items.groupby("user_id")["playtime_forever"].sum()
    df = pd.DataFrame(data).reset_index().sort_values(by="playtime_forever", ascending=False)
    most_hours_player = df.iloc[0][["user_id"]][0]

    hours_by_year = genre_items.groupby(genre_items["date"].dt.year)["playtime_forever"].sum()
    hours_by_year = [{"Año": year, "Horas": hours} for year, hours in hours_by_year.items()]

    return {"Player with most hours played for " + genre: most_hours_player,
        "Horas jugadas": hours_by_year}


@app.get("/best_developer_year/{year}")
def best_developer_year(year: int):

    developer_reviews = users_reviews.merge(steam_games[["game_id", "developer"]], on="game_id", how="left")
    developer_reviews = developer_reviews[developer_reviews["date"].dt.year == year ]

    positive_sentiment_items = developer_reviews[developer_reviews["sentiment"] == 2 ]
    
    positive_sentiment_items = positive_sentiment_items.groupby("developer")["sentiment"].count()
    positive_sentiment_items = pd.DataFrame(positive_sentiment_items).reset_index().sort_values(by="sentiment", ascending=False)

    recommended_items = developer_reviews[developer_reviews["recommend"] == True ]
    recommended_items = recommended_items.groupby("developer")["recommend"].count()
    recommended_items = pd.DataFrame(recommended_items).reset_index().sort_values(by="recommend", ascending=False)
    
    top_developers = pd.merge(positive_sentiment_items, recommended_items, on="developer")
    top_developers["recomendations"] = top_developers["sentiment"] + top_developers["recommend"]

    return [{"Position 1:": top_developers.iloc[0]["developer"]},
            {"Position 2:": top_developers.iloc[1]["developer"]},
            {"Position 3:": top_developers.iloc[2]["developer"]}]


@app.get("/developer_reviews_analysis/{developer}")
def developer_reviews_analysis(developer: str):

    developer_reviews = users_reviews.merge(steam_games[["game_id", "developer"]], on="game_id", how="left")
    developer_reviews = developer_reviews[developer_reviews["developer"] == developer ]
    sentiment_count = developer_reviews["sentiment"].value_counts()

    return {developer: [{"Negative": sentiment_count.get("Negative", 0), "Positive": sentiment_count.get("Positive", 0)}]}


@app.get("/recommend/{title}")
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
    similar_games_dict = {'recommendations': similar_game_titles}

    return similar_games_dict