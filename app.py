import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=73795d733f0236568f96f0a1d6b81be5')
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommneded_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x : x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in recommneded_movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_posters

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "Select a Movie you are interested in:",
    movies_list
)

if st.button('Recommend'):

    st.write(f"Recommending Movies based on {selected_movie}")
    recommendations, posters = recommend(selected_movie)

    cols = st.columns(len(recommendations))

    for i, col in enumerate(cols):
        with col:
            st.subheader(recommendations[i])
            st.image(posters[i])
            