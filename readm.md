## MLOps Proyect - Video Game Recommendation System

This project focuses on the creation of a video game recommendation system. This repository is the documentation of that process that includes the following stages:

01_ETL: initial data cleaning process
02_EDA: exploratory data analisys
03_ML: data preparration and system implementation
03_API: deploiment of the system and other useful information

#### 01_ETL:

In this phase, I focus on preparing the provided datasets, including steam_games.json, australian_users_reviews.json, and australian_users_items.json, for subsequent analysis and the development of recommendation systems. The data transformation process involves several key steps to ensure data quality and consistency:

Data Importation and Initial Exploration: 
I begin by importing the raw data into Pandas DataFrames.
I conduct an initial exploration to understand the basic structure and composition of each dataset.

Desanidating and Reformatting: 
I perform a desanidation process where necessary, transforming nested structures into flat data rows. This simplifies data handling and analysis.
I carefully rename and reorder columns as needed for clarity and consistency.

Handling Missing Values: 
I address missing values in the datasets to ensure data integrity and reliability. Different strategies are applied depending on the context of the data.

Dropping Repetitive and Low-Quality Columns: 
In my efforts to streamline the datasets and focus on relevant features, I identify and eliminate redundant or low-quality columns.

Preparing Data for Recommendation System: 
In this step, we focus on preparing the data specifically for our item-to-item recommendation system. We extract and categorize game genres, enabling more targeted recommendations. This involves classifying genres as popular, common, or unpopular based on their frequency in the dataset. The resulting data, stored in the 'item_to_item_model_data' DataFrame, is optimized for the development of an effective item-to-item recommendation system, enhancing the precision and relevance of game recommendations.


#### 2 - Exploratory Data Analysis (EDA):

Includes the calculation of new data, the implementation of a RESTful API and two recommendation system (user-user and user-item).


I perform a Exploratory Data Analysis (EDA) to gain deeper insights into the transformed data. I reduce the analysis process to the few variables I decide to use in the recomendation system model. EDA helps me identify patterns, outliers, and potential relationships that will inform the recommendation system's design and customization.

![Texto alternativo](gallery/EDA.gif)

In the EDA process, it was observed that some genres, such as "Action" and "Indie," constitute a significant percentage of the dataset. To optimize the item-to-item recommendation system, genres will be categorized into three groups based on their frequency:

Frequent Genres: Genres that appear frequently in the dataset. These are the most popular genres.
Moderate Genres: Genres that have a moderate presence in the dataset.
Rare Genres: Genres that appear infrequently in the dataset.


#### 3 - API Development: 

Implement a RESTful API using the FastAPI framework to provide data access and specific queries. This API provides various endpoints to access and retrieve information related to Steam games and user reviews. It utilizes the FastAPI framework and offers the following functionalities:

Playtime by Genre: (not implemented)
GET /playtime_genre/{genre}: Returns the year with the most playtime for a given genre.

User for Genre: (not implemented)
GET /user_for_genre/{genre}: Retrieves the user with the highest playtime for a given genre and provides a list of accumulated playtime by year.

Users' Top Recommendations:
GET /users_recommend/{year}: Returns the top 3 games most recommended by users for a given year.

Users' Least Recommendations:
GET /users_not_recommend/{year}: Provides the top 3 games least recommended by users for a given year.

Sentiment Analysis:
GET /sentiment_analysis/{year}: Returns a breakdown of user review records categorized by sentiment (Negative, Neutral, Positive) for a specific year.


#### 4 - Machine Learning Model:

Create at least one video game recommendation model (either item-item or user-item) and expose it through the API.

Item-to-Item Recommendation System:
This recommendation system suggests games similar to a given game based on genre similarities.
It uses TF-IDF Vectorization and cosine similarity to create similarity matrices for games with respect to popular, common, and unpopular genres.
The recommend_similar_games function takes a game title as input and returns similar games, including their combined similarity scores and genre information.

User-to-Item Recommendation System:
This recommendation system provides game recommendations to a specific user based on the preferences and ratings of similar users.
It calculates user similarity using cosine similarity based on review sentiment scores.
The Nearest Neighbors algorithm is used to identify the k most similar users to a given user.
It calculates the average ratings given by similar users to different games and suggests the top-rated games for the user.


#### Technologies

Python: The primary programming language used for data preprocessing, analysis, and modeling.

Pandas: A powerful data manipulation and analysis library used for handling and transforming datasets.

FastAPI: A modern, fast (high-performance) web framework for building APIs with Python. Used for developing the RESTful API to provide data access and specific queries.

NumPy: A fundamental package for scientific computing with Python, used for numerical operations and array handling.

scikit-learn: An open-source machine learning library for Python, used for building and evaluating machine learning models, including cosine similarity and nearest neighbors algorithms.

TF-IDF Vectorization: A text preprocessing technique used for the item-to-item recommendation system to convert game genres into numerical features.

Data Visualization Libraries: Libraries like Matplotlib or Seaborn might be used for creating data visualizations during the exploratory data analysis (EDA) phase.

JSON: Data is often stored and exchanged in JSON format, especially in the context of API development.

Git: A version control system used for tracking changes in the codebase and collaborating with others.

GitHub: A web-based platform for hosting and sharing code repositories.

Jupyter Notebook: An interactive environment for running Python code, often used for data analysis and visualization.