import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load ratings
ratings_df = pd.read_csv("netflix_ratings.csv", header=None, names=["Cust_Id", "Ratings"], usecols=[0, 1])

# Assign Movie_Id from structure
movie_ids = []
current_movie_id = None

for val in ratings_df["Cust_Id"]:
    if ":" in str(val):
        current_movie_id = int(str(val).replace(":", ""))
    movie_ids.append(current_movie_id)

ratings_df["Movie_Id"] = movie_ids
ratings_df = ratings_df.dropna()
ratings_df["Cust_Id"] = ratings_df["Cust_Id"].astype(str)

# Convert Ratings from 0–1 to 1–5 scale
ratings_df["Ratings"] = ratings_df["Ratings"].astype(float) * 5

# Create pivot table (item-user matrix)
pivot_df = ratings_df.pivot_table(index="Movie_Id", columns="Cust_Id", values="Ratings")

# Compute similarity matrix
similarity_matrix = cosine_similarity(pivot_df.fillna(0))

# Build top-k similarity dictionary
top_k = 10
similarity_dict = {}
movie_ids = pivot_df.index.tolist()

for idx, movie_id in enumerate(movie_ids):
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_k+1]
    top_similar_ids = [movie_ids[i] for i, _ in sim_scores]
    similarity_dict[movie_id] = top_similar_ids

# Save to svd_topk.pkl
with open("svd_topk.pkl", "wb") as f:
    pickle.dump({"similarity_dict": similarity_dict}, f)

print("✅ Saved top-K similar movies to svd_topk.pkl")
