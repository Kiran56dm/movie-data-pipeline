import pandas as pd
import sqlite3
import requests
import re
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise Exception("❌ OMDB_API_KEY missing in .env file")

DB_FILE = "movies.db"
SCHEMA_FILE = "schema.sql"

print("✅ Extracting MovieLens datasets...")

movies_df = pd.read_csv("data/movies.csv")
ratings_df = pd.read_csv("data/ratings.csv")

print("Movies loaded:", movies_df.shape)
print("Ratings loaded:", ratings_df.shape)

# ------------------------------------------------------
# ✅ TRANSFORM
# ------------------------------------------------------
print("\n✅ Transforming data...")

# Extract year from title
movies_df["Year"] = movies_df["title"].str.extract(r"\((\d{4})\)")
movies_df["Year"].fillna("", inplace=True)


# ------------------------------------------------------
# ✅ IMPROVED OMDB ENRICHMENT
# ------------------------------------------------------
def clean_title(title):
    title = re.sub(r"\(\d{4}\)", "", title).strip()
    title = re.sub(r"[:,]", "", title)
    return title.strip()

def try_fetch(title, year):
    base = "http://www.omdbapi.com/"

    attempts = [
        title,
        f"{title} ({year})",
        title.replace("The ", "").strip(),
        "The " + title.strip(),
        title.split(":")[0].strip(),
    ]

    for attempt in attempts:
        r = requests.get(base, params={"t": attempt, "apikey": OMDB_API_KEY}).json()
        if r.get("Response") == "True":
            return r

    return None

def fetch_omdb(title, year=""):
    cleaned = clean_title(title)
    return try_fetch(cleaned, year)


# ------------------------------------------------------
# ✅ ENRICH ONLY FIRST 15 MOVIES
# ------------------------------------------------------
print("\n⏳ Fetching OMDb API data (first 15 movies)...")

enriched_rows = []
sample_movies = movies_df.head(15)

for _, row in sample_movies.iterrows():
    movieId = row["movieId"]
    title = row["title"]
    year = row["Year"]

    print(f"Fetching: {title}")

    omdb = fetch_omdb(title, year)

    if not omdb:
        print(f"⚠️ Not found: {title}")
        continue

    enriched_rows.append({
        "movieId": movieId,
        "title": title,
        "genres": row["genres"],
        "Year": year,
        "movielens_avg_rating": ratings_df[ratings_df["movieId"] == movieId]["rating"].mean(),
        "Director": omdb.get("Director", ""),
        "imdbRating": omdb.get("imdbRating", ""),
        "Runtime": omdb.get("Runtime", ""),
        "Genre_OMDB": omdb.get("Genre", ""),
    })

enriched_df = pd.DataFrame(enriched_rows)
print("\n✅ Enriched movies:", enriched_df.shape)



# ------------------------------------------------------
# ✅ LOAD INTO SQLITE DATABASE
# ------------------------------------------------------
print("\n✅ Creating database & loading data...")

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Run schema
with open(SCHEMA_FILE, "r") as f:
    cur.executescript(f.read())

movies_df.to_sql("movies", conn, if_exists="replace", index=False)
ratings_df.to_sql("ratings", conn, if_exists="replace", index=False)
enriched_df.to_sql("movies_enriched", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("\n🎉 ETL Completed Successfully!")
print("✅ movies.db is ready.")
