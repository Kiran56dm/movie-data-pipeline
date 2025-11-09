CREATE TABLE IF NOT EXISTS movies (
    movieId INTEGER PRIMARY KEY,
    title TEXT,
    genres TEXT,
    Year TEXT
);

CREATE TABLE IF NOT EXISTS ratings (
    userId INTEGER,
    movieId INTEGER,
    rating REAL,
    timestamp INTEGER
);

CREATE TABLE IF NOT EXISTS movies_enriched (
    movieId INTEGER PRIMARY KEY,
    title TEXT,
    genres TEXT,
    Year TEXT,
    movielens_avg_rating REAL,
    Director TEXT,
    imdbRating TEXT,
    Runtime TEXT,
    Genre_OMDB TEXT
);

