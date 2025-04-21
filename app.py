# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# from huggingface_hub import hf_hub_download
#
#
# REPO_ID = "LLawlietBLANK/Movie-Recommender-System-v1"
#
# @st.cache_resource
# def load_similarity():
#     file_path = hf_hub_download(
#         repo_id=REPO_ID,
#         filename="similarity.pkl",
#         repo_type="dataset"
#     )
#     with open(file_path, "rb") as f:
#         return pickle.load(f)
#
# @st.cache_data
# def load_movies():
#     file_path = hf_hub_download(
#         repo_id=REPO_ID,
#         filename="movie_dict.pkl",
#         repo_type="dataset"
#     )
#     with open(file_path, "rb") as f:
#         movie_dict = pickle.load(f)
#     return pd.DataFrame(movie_dict)
#
# similarity = load_similarity()
# movies = load_movies()
#
#
# # def fetch_poster(movie_id):
# #     url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2b77016502908b1d4f0ed6f99e109849&language=en-US'
# #     response = requests.get(url)
# #     data = response.json()
# #     poster_path = data.get('poster_path')
# #     if poster_path:
# #         return f"https://image.tmdb.org/t/p/w500{poster_path}"
# #     else:
# #         return "https://via.placeholder.com/500x750?text=No+Image"
#
# def fetch_poster(movie_id):
#     proxy_url = f"https://tmdb-proxy-uqi6.onrender.com/{movie_id}"
#     try:
#         response = requests.get(proxy_url)
#         data = response.json()
#         poster_path = data.get("poster_path")
#         if poster_path:
#             return f"https://image.tmdb.org/t/p/w500{poster_path}"
#         else:
#             return "https://via.placeholder.com/500x750?text=No+Image"
#     except:
#         return "https://via.placeholder.com/500x750?text=No+Image"
#
#
#
#
# def recommend(selected_movie_name):
#     movie_index = movies[movies["title"] == selected_movie_name].index[0]
#     distances = similarity[movie_index]
#     movie_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:11]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#
#     for i in movie_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#
#         # fetch movie poster from api
#         #recommended_movies_posters.append(fetch_poster(movie_id))
#         recommended_movies_posters.append(fetch_poster(movie_id))
#
#     return recommended_movies, recommended_movies_posters
#
#
#
# r = requests.get("https://api.themoviedb.org/3/movie/550?api_key=2b77016502908b1d4f0ed6f99e109849&language=en-US")
# print(r.status_code)
# print(r.json())
#
# st.title("Movie Recommender System")
# selected_movie_name = st.selectbox("Movies list", (movies['title'].values))
#
# if st.button("Recommend"):
#     names , posters = recommend(selected_movie_name)
#     cols = st.columns(5)
#     for i in range(5):
#         with cols[i]:
#             st.text(names[i])
#             st.image(posters[i])
#     cols2 = st.columns(5)
#     for i in range(5, 10):
#         with cols2[i - 5]:
#             st.text(names[i])
#             st.image(posters[i])
#


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

def fetch_poster(movie_id: int) -> str:
    proxy_url = f"https://tmdb-proxy-uqi6.onrender.com/{movie_id}"
    try:
        response = requests.get(proxy_url)
        data = response.json()
        poster_path = data.get("poster_path")
        return poster_path


    #     if poster_path:
    #         return f"https://image.tmdb.org/t/p/w500{poster_path}"
    #     else:
    #         return "https://via.placeholder.com/500x750?text=No+Image"
    # except Exception as e:
    #     print(f"Error fetching poster for movie ID {movie_id}: {e}")
    #     return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(selected_movie_name: str):
    movie_index = movies[movies["title"] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    recommended_indices = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:11]

    recommended_titles = []
    recommended_posters = []

    for i in recommended_indices:
        movie_data = movies.iloc[i[0]]
        movie_id = movie_data.movie_id
        recommended_titles.append(movie_data.title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters

# UI
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox("Select a movie you like:", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
    cols2 = st.columns(5)
    for i in range(5, 10):
        with cols2[i - 5]:
            st.text(names[i])
            st.image(posters[i])
