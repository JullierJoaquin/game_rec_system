## MLOps Project - Video Game Recommendation System

This repository documents the development of a video game recommendation system. The project is organized into the following key stages:

- [01_ETL](01_ETL.ipynb): Initial data cleaning scripts.

- [02_EDA](02_EDA.ipynb): Exploratory data analysis notebooks.

- [03_ML](03_ML.ipynb): Data preparation and recommendation system implementation.

- [04_API](04_API.ipynb): Deployment files for the recommendation system [API](main.py).


#### 01_ETL:

This stage involves the data initial exploration and transformation.


#### 02_EDA:

Exploration of the data to identify patterns and understand the characteristics of the video game dataset.


#### 03_ML:

Prepare the data for machine learning and developing the recommendation system.


#### 04_API:

Using the FastAPI framework this API provides various endpoints to access and retrieve information related to Steam games and user reviews and to the recommendation system trough the following endpoins:

GET /developer/{developer}: Returns the amount of items and free contet porcentage for a given developer.

GET /userdata/{user_id}: Returns the total spent money, the recomendation percentage and the total amount of items for a given user.

GET /user_for_genre/{genre}: Returns the user with the highest playtime for a given genre and provides a list of accumulated playtime by year.

GET /best_developer_year/{year}: Returns the top 3 developer most recommended by users for a given year.

GET /developer_reviews_analysis/{developer}: Returns the positive and negative sentiment count for a given developer.



GET /sentiment_analysis/{year}: Returns a breakdown of user review records categorized by sentiment (Negative, Neutral, Positive) for a specific year.


#### Files
    
The files include...

- [data](data/): 
- [gallery](gallery/):
- [lib](lib/:)


#### License

This project is licensed under the [MIT License](LICENSE).


#### Contact

Feel free to contact: julliercapellojoaquin@gmail.com