import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load and preprocess data from combined_data_1.txt
data_path = "combined_data_1.txt"
ratings_list = []

with open(data_path, "r") as f:
    movie_id = None
    for line in f:
        line = line.strip()
        if line.endswith(":"):
            movie_id = int(line.replace(":", ""))
        else:
            try:
                user_id, rating, _ = line.split(",")
                ratings_list.append([int(user_id), int(movie_id), float(rating)])
            except:
                continue

ratings_df = pd.DataFrame(ratings_list, columns=["Cust_Id", "Movie_Id", "Ratings"])

# Filter active users and popular movies (60th percentile)
movie_counts = ratings_df['Movie_Id'].value_counts()
movie_thresh = movie_counts.quantile(0.6)
ratings_df = ratings_df[ratings_df['Movie_Id'].isin(movie_counts[movie_counts >= movie_thresh].index)]

user_counts = ratings_df['Cust_Id'].value_counts()
user_thresh = user_counts.quantile(0.6)
ratings_df = ratings_df[ratings_df['Cust_Id'].isin(user_counts[user_counts >= user_thresh].index)]

# Create pivot table: rows = movies, columns = users (to reduce memory)
pivot_table = ratings_df.pivot_table(index='Movie_Id', columns='Cust_Id', values='Ratings').fillna(0)

# Apply TruncatedSVD
svd = TruncatedSVD(n_components=20, random_state=42)
latent_matrix = svd.fit_transform(pivot_table)

# Compute cosine similarity between movies
similarity = cosine_similarity(latent_matrix)

# Save both model and pivot info
with open("svd_model.pkl", "wb") as f:
    pickle.dump({
        "svd_model": svd,
        "item_user_matrix": pivot_table,
        "similarity": similarity
    }, f)

print("✅ Model trained and saved as svd_model.pkl")
