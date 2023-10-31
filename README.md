## MLOps Project - Video Game Recommendation System

This repository documents the development of a video game recommendation system. The project is organized into the following key stages:

[01_ETL](01_ETL.ipynb): Initial data cleaning and exploration.

[02_EDA](02_EDA.ipynb): Exploratory data analysis.

[03_ML](03_ML.ipynb): Data preparation and recommendation system implementation.

[04_API](04_API.ipynb): Deployment for the recommendation system and other useful information.


#### [01_ETL:](01_ETL.ipynb) Initial data cleaning and exploration.

This stage involves the data initial exploration and transformation of the three main datasets:
steam_games, australian_users_reviews, and australian_users_items, for subsequent analysis and the development of recommendation systems.

![ETL.jpg](/gallery/ETL/ETL.jpg)

#### [02_EDA:](02_EDA.ipynb) Exploratory data analysis.

I perform an Exploratory Data Analysis (EDA) to gain deeper insights into the transformed data. I reduce the analysis process to the few variables I decide to use in the recommendation system model. EDA helps me identify patterns, outliers, and potential relationships that will inform the recommendation system's design and customization.

![EDA.gif](/gallery/EDA/eda_gif.gif)


#### [03_ML:](03_ML.ipynb) Data preparation and recommendation system implementation.

Prepare the data for machine learning and develop an Item-to-Item Recommendation System. The recommendation system suggests games similar to a given game based on genre similarities, using TF-IDF Vectorization and cosine similarity to create similarity matrices for games with respect to popular, common, and unpopular genres after filtering the games by score, price, and year.

#### [04_API:](04_API.ipynb) Deployment for the recommendation system and other useful information.

Using the FastAPI frameworkv this [API](https://pi-ml-ops-iviw.onrender.com/) provides various endpoints to access and retrieve information related to Steam games and user reviews and the recommendation system through the following endpoints:

[GET /developer/{developer}](https://pi-ml-ops-iviw.onrender.com/developer/Valve): Returns the amount of items and free contet porcentage for a given developer.

[GET /userdata/{user_id}](https://pi-ml-ops-iviw.onrender.com/userdata/76561197970982479): Returns the total spent money, the recomendation percentage and the total amount of items for a given user.

[GET /user_for_genre/{genre}](https://pi-ml-ops-iviw.onrender.com/user_for_genre/Action): Returns the user with the highest playtime for a given genre and provides a list of accumulated playtime by year.

[GET /best_developer_year/{year}](https://pi-ml-ops-iviw.onrender.com/best_developer_year/2013): Returns the top 3 developer most recommended by users for a given year.

[GET /developer_reviews_analysis/{developer}](https://pi-ml-ops-iviw.onrender.com/developer_reviews_analysis/Ubisoft): Returns the positive and negative sentiment count for a given developer.

[GET /recommend_game/{game_id}](https://pi-ml-ops-iviw.onrender.com/recommend_game/10): Returns a list of 5 similar games for a given game id.


#### Libraries and tools

- Python: Primary programming language for data preprocessing, analysis, and modeling.
- Jupyter Notebook: Interactive environment for running Python code.
- Pandas: Data manipulation and analysis.
- FastAPI: Web framework for building RESTful APIs.
- NumPy: Python library for numerical operations and array handling.
- scikit-learn: Machine learning Python library.
- Matplotlib and Seaborn: Data visualization
- Git: Tracking changes in the codebase and collaborating with others.


#### Files
    
The files include...

- [data](data/): Here, you can find the unprocessed and processed data files.

- [gallery](gallery/): Here I store all the data visualizations in png format.

- [lib](lib/:)  Here, I store some recurring visualizations and transformations.


#### Contact

Feel free to contact: julliercapellojoaquin@gmail.com