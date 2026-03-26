import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(layout=None)

with open(r"moviesimilarity.pkl", 'rb') as file:
  similarity = pickle.load(file)

df = pd.read_csv(r'tmdbdf.csv')
df = df.head(5000)

st.image('image.jpg', width='stretch')
st.title("🍿Netflix Movie Recommendation")

# Movie Selection
movie_name = st.selectbox('Select the Movie', df['title'].values)

def recommendation(movie):
    movie_index = df[df['title']==movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movie = []
    recommend_poster = []

    for i in movie_list:
      recommend_movie.append(df.iloc[i[0]].title)
      poster = df.iloc[i[0]]['poster_path']
      if pd.notnull(poster):
        recommend_poster.append("https://image.tmdb.org/t/p/w500" + poster)

    return recommend_poster, recommend_movie


if st.button("Show related Movies"):
  posters, names = recommendation(movie_name)
  cols = st.columns(5)
  for idx, col in enumerate(cols):
      with col:
          st.image(posters[idx])
          st.subheader(names[idx])