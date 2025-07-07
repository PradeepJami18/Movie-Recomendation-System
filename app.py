import streamlit as st
import pandas as pd
import pickle
import tmdbsimple as tmdb
import math
import os
import gdown

# --- TMDB API KEY ---
tmdb.API_KEY = st.secrets["TMDB_API_KEY"]

# --- Download the model from Google Drive if not present ---
model_file = "svd_model.pkl"
gdrive_file_id = "1FThLRfPXf-cbn0spzZSl4OY7zb2nEc-K"

if not os.path.exists(model_file):
    url = f"https://drive.google.com/uc?id={gdrive_file_id}"
    gdown.download(url, model_file, quiet=False)

# --- Load model and data ---
with open(model_file, "rb") as f:
    data = pickle.load(f)

svd_model = data["svd_model"]
item_user_matrix = data["item_user_matrix"]
similarity_matrix = data["similarity"]

# ✅ Convert ratings from 0–1 scale to 1–5
item_user_matrix = item_user_matrix * 4 + 1

# --- Load movie metadata ---
movie_titles_df = pd.read_csv(
    "movie_titles.csv", 
    encoding="ISO-8859-1", 
    header=None, 
    names=["Movie_Id", "Year", "Title"], 
    usecols=[0, 1, 2]
)
movie_id_to_title = dict(zip(movie_titles_df.Movie_Id, movie_titles_df.Title))
movie_id_to_year = dict(zip(movie_titles_df.Movie_Id, movie_titles_df.Year))
common_ids = [mid for mid in item_user_matrix.index if mid in movie_id_to_title]

# --- TMDB Poster Fetcher ---
def fetch_poster(movie_name):
    try:
        search = tmdb.Search()
        response = search.movie(query=movie_name)
        if response['results']:
            poster_path = response['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w200{poster_path}"
    except Exception as e:
        print("Poster fetch error:", e)
    return None

# --- Star Renderer ---
def render_stars(rating):
    full = "⭐" * int(round(rating))
    empty = "☆" * (5 - int(round(rating)))
    return full + empty

# --- Recommendation function ---
def get_recommendations(movie_id, top_n=10):
    if movie_id not in common_ids:
        return []
    idx = common_ids.index(movie_id)
    scores = list(enumerate(similarity_matrix[idx]))
    top_indices = sorted(scores, key=lambda x: x[1], reverse=True)[1: top_n+1]
    return [common_ids[i] for i, _ in top_indices]

# --- Streamlit UI ---
st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")

# Dropdown using movie titles
selected_title = st.selectbox("Choose a movie to find similar ones", 
                              options=[movie_id_to_title[mid] for mid in common_ids])

# Map title back to ID
selected_movie_id = movie_titles_df[
    movie_titles_df.Title == selected_title
]['Movie_Id'].values[0]

if st.button("Get Recommendations"):
    rec_ids = get_recommendations(selected_movie_id)
    if not rec_ids:
        st.warning("No similar movies found!")
    else:
        st.subheader(f"Top {len(rec_ids)} movies like **{selected_title}**:")
        for mid in rec_ids:
            title = movie_id_to_title.get(mid, "Unknown")
            year = movie_id_to_year.get(mid, "N/A")
            poster = fetch_poster(title)
            avg_rating = item_user_matrix.loc[mid].mean()
            avg_rating = round(avg_rating, 2)
            stars = render_stars(avg_rating)

            col1, col2 = st.columns([1, 4])
            with col1:
                if poster:
                    st.image(poster, width=100)
            with col2:
                st.markdown(f"**🎬 {title}** ({year})")
                st.markdown(f"{stars} — **{avg_rating}/5**")
