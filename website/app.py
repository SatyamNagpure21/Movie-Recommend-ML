import pandas as pd
import streamlit as st
import pickle
import requests
#
# url = "https://api.themoviedb.org/3/account/22316078"
#
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MWM1NTExMzZjMGVlOWUzYzg2M2RjN2M2YWY3NmZlMSIsIm5iZiI6MTc1ODA1NTU3NS40NjIwMDAxLCJzdWIiOiI2OGM5Y2M5NzAxMDU1NjhlNmI3OGMyYjMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.fhUT8unxzFjWsAtgqHLNc0egWg6XNQVla4-l_dPrrdY"
}

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=1c4c6a940baefc89c225d5942a4a34e0&language=en-US"
    response = requests.get(url)
    data = response.json()

    # check if 'poster_path' exists
    if 'poster_path' in data and data['poster_path'] is not None:
        return "https://image.tmdb.org/t/p/original/" + data['poster_path']
    else:
        # fallback image if no poster is available
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    # response = requests.get(url.format(movie_id), headers=headers)
    # data = response.json()
    # return "https://image.tmdb.org/t/p/original/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommend_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies,recommend_movies_posters

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')


selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


