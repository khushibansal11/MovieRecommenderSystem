import streamlit as st
import pickle
import requests
import pandas as pd

st.title("Movie Recommender System")
movies_dataset=pickle.load(open('movie_list.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

movies_list=movies_dataset['title'].unique()
movie_selected=st.selectbox("Select movie name",movies_list)

def poster(id):
    print(id)
    url = f'https://api.themoviedb.org/3/movie/{id}?api_key=8361095de50c93214b053b4d4e8fed5f&language=en-US'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching poster for ID {id}: {response.status_code}")
        return 'https://via.placeholder.com/300x450?text=No+Image'

    data = response.json()
    poster_path = data.get('poster_path')

    if poster_path:
        return 'https://image.tmdb.org/t/p/original' + poster_path
    else:
        print(f"No poster path for movie ID {id}")
        return 'https://via.placeholder.com/300x450?text=No+Image'


def recommend(movie):
    recommended_titles = []
    recommended_ids = []
    movie_index = movies_dataset[movies_dataset['title'] == movie].index[0]
    recommended_index = sorted(enumerate(similarity[movie_index]), key=lambda x: x[1], reverse=True)[1:6]

    for i in recommended_index:
        recommended_titles.append(movies_dataset.iloc[i[0]].title)
        recommended_ids.append(movies_dataset.iloc[i[0]].movie_id)  

    return recommended_ids, recommended_titles


movie_list,result=recommend(movie_selected)
col1,col2,col3,col4,col5=st.columns(5)
with col1:
    st.write(result[0])
    st.image(poster(movie_list[0]))
with col2:
    st.write(result[1])
    st.image(poster(movie_list[1]))
with col3:
    st.write(result[2])
    st.image(poster(movie_list[2]))
with col4:
    st.write(result[3])
    st.image(poster(movie_list[3]))
with col5:
    st.write(result[4])
    st.image(poster(movie_list[4]))
