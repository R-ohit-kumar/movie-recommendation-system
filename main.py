import streamlit as st
import pickle
import pandas as pd
import requests


# def fetch_poster(movie_id):
#     response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key=6b4483f5219761ef0bf431e296881af5")
#     data = response.json()
#     # st.text(data)
#     try:
#         poster_url = "http://image.tmdb.org/t/p/w500/" + data["posters"][1]["file_path"]
#     except:
#         poster_url = "http://image.tmdb.org/t/p/w500/" + data["posters"][0]["file_path"]
#
#     return poster_url


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key=6b4483f5219761ef0bf431e296881af5"
    try:
        # Add timeout and retry-safe call
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error if response != 200

        data = response.json()
        posters = data.get("posters", [])

        if len(posters) >= 2:
            poster_path = posters[1]["file_path"]
        elif len(posters) == 1:
            poster_path = posters[0]["file_path"]
        else:
            # No posters found
            return "https://via.placeholder.com/500x750?text=No+Poster"

        return f"https://image.tmdb.org/t/p/w500/{poster_path}"

    except requests.exceptions.RequestException as e:
        print(f"Network error for movie ID {movie_id}: {e}")
        # Fallback image if API fails or connection drops
        return "https://via.placeholder.com/500x750?text=Poster+Error"



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies_lists = movies['title'].values
st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Select a Movie", movies_lists)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3 = st.columns(3)
    col4, col5,col6 = st.columns(3)


    with col1:
        st.subheader(names[0])
        st.image(posters[0])

    with col2:
        st.subheader(names[1])
        st.image(posters[1])

    with col3:
        st.subheader(names[2])
        st.image(posters[2])

    with col4:
        st.subheader(names[3])
        st.image(posters[3])

    with col5:
        st.subheader(names[4])
        st.image(posters[4])


