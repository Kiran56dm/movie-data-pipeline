import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# 1. Highest average rating
print("\n1️⃣ Highest Rated Movie:")
cursor.execute("""
SELECT m.title, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.movieId
ORDER BY avg_rating DESC
LIMIT 1;
""")
print(cursor.fetchall())

# 2. Top 5 genres
print("\n2️⃣ Top 5 Genres:")
cursor.execute("""
WITH split_genres AS (
    SELECT 
        m.movieId,
        TRIM(value) AS genre
    FROM movies m,
         json_each('["' || replace(m.genres, '|', '","') || '"]')
),
avg_genre_rating AS (
    SELECT 
        sg.genre,
        AVG(r.rating) AS avg_rating
    FROM split_genres sg
    JOIN ratings r ON sg.movieId = r.movieId
    GROUP BY sg.genre
)
SELECT genre, avg_rating
FROM avg_genre_rating
ORDER BY avg_rating DESC
LIMIT 5;
""")
print(cursor.fetchall())

# 3. Director with most movies
print("\n3️⃣ Director With Most Movies:")
cursor.execute("""
SELECT Director, COUNT(*) AS total_movies
FROM movies_enriched
WHERE Director IS NOT NULL AND Director != ''
GROUP BY Director
ORDER BY total_movies DESC
LIMIT 1;
""")
print(cursor.fetchall())

# 4. Average rating per year
print("\n4️⃣ Avg Rating Per Year:")
cursor.execute("""
WITH avg_ratings AS (
    SELECT movieId, AVG(rating) AS avg_rating
    FROM ratings
    GROUP BY movieId
)
SELECT e.Year, AVG(a.avg_rating)
FROM movies_enriched e
JOIN avg_ratings a ON e.movieId = a.movieId
WHERE e.Year IS NOT NULL AND e.Year != ''
GROUP BY e.Year
ORDER BY e.Year;
""")
print(cursor.fetchall())

conn.close()
