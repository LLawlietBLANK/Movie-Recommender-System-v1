import streamlit as st
import pickle
import pandas as pd
import requests
from huggingface_hub import hf_hub_download


REPO_ID = "LLawlietBLANK/Movie-Recommender-System-v1"

@st.cache_resource
def load_similarity():
    file_path = hf_hub_download(
        repo_id=REPO_ID,
        filename="similarity.pkl",
        repo_type="dataset"
    )
    with open(file_path, "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_movies():
    file_path = hf_hub_download(
        repo_id=REPO_ID,
        filename="movie_dict.pkl",
        repo_type="dataset"
    )
    with open(file_path, "rb") as f:
        movie_dict = pickle.load(f)
    return pd.DataFrame(movie_dict)

similarity = load_similarity()
movies = load_movies()


def recommend(selected_movie_name):
    movie_index = movies[movies["title"] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:11]

    recommended_movies = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


st.title("Movie Recommender System")
selected_movie_name = st.selectbox("Movies list", (movies['title'].values))

if st.button("Recommend"):
    recommendations = recommend(selected_movie_name)
    #col = st.columns(10)
    st.write(recommendations)
