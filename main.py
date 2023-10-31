import ast
import fastapi
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Instanciate objects
vectorizer = TfidfVectorizer()
app = fastapi.FastAPI()

# Import and process data
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


@app.get("/") # Returns a confirmation message and the available endpoints
def test():
    return {"API STEAM GAMES ACTIVE"
            "endpoints": {
                "/developer/{developer}": "Valve",
                "/user_data/{user_id}": "76561197970982479",
                "/user_for_genre/{genre}": "Action",
                "/best_developer_year/{year}": 2010,
                "/developer_reviews_analysis/{developer}": "Ubisoft",
                "/recommend/{title}": "Counter-Strike"}}



@app.get("/developer/{developer}") # Returns the amount of items and free contet porcentage for a given developer
def developer(developer: str):
    # Filter data
    developer_data = steam_games[steam_games["developer"] == developer]
    if developer_data.empty:
        return {"error": "Developer not found"}
    # Find amount of items per year
    game_count_by_year = developer_data["date"].dt.year.value_counts()
    game_count_by_year_df = pd.DataFrame(game_count_by_year).reset_index()
    game_count_by_year_df.columns = ["year", "item_count"]
    # Find amount of free items per year
    free_game_count_by_year = developer_data["date"][developer_data["price"] == 0].dt.year.value_counts()
    free_game_count_by_year_df = pd.DataFrame(free_game_count_by_year).reset_index()
    free_game_count_by_year_df.columns = ["year", "free_item_count"]
    # Create dataframe and calculate free content percentage
    game_count_by_year_df = pd.merge(game_count_by_year_df, free_game_count_by_year_df, on="year", how="left")    
    game_count_by_year_df["free_content"] = game_count_by_year_df["free_item_count"] * 100 / game_count_by_year_df["item_count"]
    game_count_by_year_df.drop(columns="free_item_count", inplace=True)
    game_count_by_year_df["free_content"].fillna(0, inplace=True)
    # Create JSON and return
    list = []
    for i, row in game_count_by_year_df.iterrows():
        list.append({"Year": row["year"], "Total items": row["item_count"], "Free content": row["free_content"]})
    return {"Developer": developer, "Items by year:": list}



@app.get("/userdata/{user_id}") # Returns the total spent money, the recomendation percentage and the total amount of items for a given user
def userdata(user_id: str):
    # Filter data
    user_items = users_items[users_items["user_id"] == user_id ]
    user_reviews = users_reviews[users_reviews["user_id"] == user_id]
    # Calculate spented money
    user_items = user_items.merge(steam_games[["game_id", "price"]], on="game_id", how="left")    
    spent_money = user_items["price"].sum()
    # Calculate item amount and recommendatio rate
    item_count = user_reviews.shape[0]
    recommend_rate = user_reviews["recommend"].value_counts()[True] * 100 / item_count

    return {"user_id": user_id, "spent_money": spent_money, "recommend_rate": recommend_rate, "item_count": item_count}



@app.get("/userforgenre/{genre}") # Returns the user with the highest playtime and a list of accumulated playtime by year for a given genre 
def UserForGenre(genre: str):
    # Filter data
    genre_items = users_items.merge(steam_games[["genres", "game_id", "date"]], on="game_id", how="left")
    genre_items["genres"] = genre_items["genres"].fillna("[]")
    genre_items = genre_items[genre_items["genres"].apply(lambda x: genre in x)]
    if genre_items.empty:
        return {"error": f"No records found for genre: {genre}"}
    # Calculate player with most hours played
    data = genre_items.groupby("user_id")["playtime_forever"].sum()
    df = pd.DataFrame(data).reset_index().sort_values(by="playtime_forever", ascending=False)
    most_hours_player = df.iloc[0][["user_id"]][0]
    # Calculate playtime for each year
    hours_by_year = genre_items.groupby(genre_items["date"].dt.year)["playtime_forever"].sum()
    hours_by_year = pd.DataFrame(hours_by_year).reset_index()
    hours_by_year.columns = ["year", "playtime"]
    # Creat JSON and return
    list = []
    for i, row in hours_by_year.iterrows():
        list.append({"Year": row["year"], "playtime": row["playtime"]})
    return {"Top player": most_hours_player,
        "Hours played by year": list}



@app.get("/best_developer_year/{year}") # Returns the top 3 developer most recommended by users for a given year
def best_developer_year(year: int):
    # Filter data
    developer_reviews = users_reviews.merge(steam_games[["game_id", "developer"]], on="game_id", how="left")
    developer_reviews = developer_reviews[developer_reviews["date"].dt.year == year ]
    if developer_reviews.empty:
        return {"error": f"No records found for year: {year}"}
    # Count recommendations
    positive_sentiment_items = developer_reviews[developer_reviews["sentiment"] == 2 ]
    positive_sentiment_items = positive_sentiment_items.groupby("developer")["sentiment"].count()
    positive_sentiment_items = pd.DataFrame(positive_sentiment_items).reset_index().sort_values(by="sentiment", ascending=False)
    # Count positive analysis
    recommended_items = developer_reviews[developer_reviews["recommend"] == True ]
    recommended_items = recommended_items.groupby("developer")["recommend"].count()
    recommended_items = pd.DataFrame(recommended_items).reset_index().sort_values(by="recommend", ascending=False)
    # Sort by total score and return the top 3 developers
    top_developers = pd.merge(positive_sentiment_items, recommended_items, on="developer")
    top_developers["recomendations"] = top_developers["sentiment"] + top_developers["recommend"]
    return {"Position 1": top_developers.iloc[0]["developer"],
        "Position 2": top_developers.iloc[1]["developer"],
        "Position 3": top_developers.iloc[2]["developer"]}



@app.get("/developer_reviews_analysis/{developer}") # Returns the positive and negative sentiment count for a given developer
def developer_reviews_analysis(developer: str):
    # Filter data
    developer_reviews = users_reviews.merge(steam_games[["game_id", "developer"]], on="game_id", how="left")
    developer_reviews = developer_reviews[developer_reviews["developer"] == developer ]
    if developer_reviews.empty:
        return {"error": f"No records found for developer: {developer}"}
    # Calculate positive and negative sentiment and return
    sentiment_count = developer_reviews["sentiment"].value_counts()
    return {"Negative": sentiment_count[0],
            "Positive": sentiment_count[2]}



@app.get("/recommend/{title}") # Returns a list of 5 games recommendations for a given title 
def recommend_similar_games(title):
    # Find game index
    game_index = model_data[model_data['title'] == title].index[0]
    # Filter games bases on date
    year = model_data["date"].dt.year[game_index]
    five_years_ago = year - 5
    five_years_later = year + 5
    filtered_data = model_data[(model_data["date"].dt.year >= five_years_ago) & (model_data["date"].dt.year <= five_years_later)]
    # Filter games based on price
    price = model_data["price_discr"][game_index]
    upper_price = price + 1
    lower_price = price - 1
    filtered_data = filtered_data[(filtered_data["price_discr"] >= lower_price) & (filtered_data["price_discr"] <= upper_price)]
    # Filter games based on score
    score = model_data["score"][game_index]
    upper_score = score + 1
    lower_score = score - 1
    filtered_data = filtered_data[(filtered_data["score"] >= lower_score) & (filtered_data["score"] <= upper_score)]
    # Find new game index
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
    # Combine the similarity matrices for the three genre categories with choosen importance
    similarity_matrix = popular_genres_similarity_matrix + common_genres_similarity_matrix * 1.5 + unpopular_genres_similarity_matrix * 2
    # Adjust the game indices for the filtered_data
    similar_game_indices = similarity_matrix[new_game_index].argsort()[::-1][1:6]
    # Obtain the names of similar games and their similarity scores
    similar_game_scores = similarity_matrix[new_game_index][similar_game_indices]
    similar_game_titles = filtered_data.iloc[similar_game_indices]['title'].tolist()
    # Create a DataFrame with titles and similarity scores
    similar_games_dict = {'recommendations': similar_game_titles}
    return similar_games_dict