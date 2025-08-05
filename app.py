import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=10de773eb6ab694faa5b65ee5af9d7cd&language=en-US"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = Movies[Movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        # ✅ Use correct column name based on your DataFrame
        movie_id = Movies.iloc[i[0]]['movie_id']  # change 'movie_id' to whatever column is correct
        recommended_movies.append(Movies.iloc[i[0]]['title'])
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


# Load data
movies_dict = pickle.load(open('moviedict.pkl', 'rb'))
Movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('sim.pkl', 'rb'))

# Streamlit UI
st.title('Movies Recommender')

option = st.selectbox('How would you like to recommend movies?', Movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(option)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
