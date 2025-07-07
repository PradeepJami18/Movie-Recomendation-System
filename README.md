# 🎬 Movie Recommendation System

A smart recommendation engine that suggests similar movies based on a selected title using collaborative filtering (SVD). Built with **Streamlit**, it fetches **posters**, displays **release year**, and visualizes **ratings using stars** — all powered by the **TMDB API**.

---

## 🧠 Overview

This app enables users to select a movie and receive top 10 recommendations based on a similarity matrix trained on Netflix movie ratings. It uses:

- **SVD (Singular Value Decomposition)** for latent factor modeling
- **Cosine similarity** for identifying similar movies
- **TMDB API** for fetching posters and metadata
- **Streamlit** for an interactive UI

---

## 📸 Sample Output

<img src="screenshots/sample_ui.png" width="800" alt="App Screenshot">

---

## 📁 Folder Structure

```
📦 Movie-Recommender/
├── app.py                   # Streamlit app
├── svd_model.pkl            # Trained model with similarity matrix
├── movie_titles.csv         # Metadata with Movie_Id, Title, Year
├── netflix_ratings.csv      # Ratings (0–1 format)
├── requirements.txt         # Python dependencies
├── .streamlit/
│   └── secrets.toml         # API key storage (TMDB)
└── screenshots/
    └── sample_ui.png        # UI Preview
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/PradeepJami18/movie-recommender.git
cd movie-recommender
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your TMDB API Key

Create the following file:

```
.movie-recommender/
└── .streamlit/
    └── secrets.toml
```

Inside `secrets.toml`, paste your TMDB API key like this:

```toml
TMDB_API_KEY = "your_tmdb_api_key_here"
```

> 📌 [Get your TMDB API Key](https://developer.themoviedb.org/docs/getting-started)

---

## 🚀 Running the App Locally

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💫 Features

- 🎞️ Poster support via **TMDB API**
- 🌟 Ratings visualized as 5-star bars (0–1 scaled to 1–5)
- 📅 Movie release year display
- ⚡ Fast response with precomputed similarity matrix
- 🧊 Clean & responsive Streamlit UI

---

## 📦 Requirements

```txt
streamlit
pandas
numpy
scikit-learn
tmdbsimple
```

Install using:

```bash
pip install -r requirements.txt
```

---

## 🌐 Deployment (Optional)

You can deploy this app on [Streamlit Community Cloud](https://streamlit.io/cloud).

1. Push your code to a GitHub repo.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect your repo.
3. Add your **TMDB API key** in **App Settings > Secrets** like this:

```toml
TMDB_API_KEY = "your_tmdb_api_key"
```

---

## 🙋‍♂️ Author

**Jami Pradeep**  
📧 pradeepjami18@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/jami-pradeep-95b68036a)  
📁 [GitHub](https://github.com/PradeepJami18)

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more information.

---

## 📌 Future Improvements

- Add genre-based filtering
- Incorporate user authentication
- Add rating and review submission from users
- Real-time retraining with feedback

---

> 💡 If you like this project, feel free to ⭐ it on GitHub!
