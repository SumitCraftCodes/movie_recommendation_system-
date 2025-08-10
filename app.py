import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.parse

# Function to fetch movie poster from OMDb API
def fetch_poster(movie_title):
    cleaned_title = urllib.parse.quote(movie_title.strip())
    url = f"http://www.omdbapi.com/?t={cleaned_title}&apikey=bfd22a8e"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_url = data.get('Poster')
        if poster_url and poster_url != "N/A":
            return poster_url
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = i[0]
        recommended_movie_names.append(movies.iloc[movie_id].title)
        recommended_movie_posters.append(fetch_poster(movies.iloc[movie_id].title))
    return recommended_movie_names, recommended_movie_posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

if st.button('Recommend'):
    
    names, posters = recommend(selected_movie_name)

    # Display 5 recommended movies and posters
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
