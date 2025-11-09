-- 1. Which movie has the highest average rating?
SELECT m.title, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.movieId
ORDER BY avg_rating DESC
LIMIT 1;

-- 2. Top 5 genres with highest average rating
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

-- 3. Director with most movies
SELECT Director, COUNT(*) AS total_movies
FROM movies_enriched
WHERE Director IS NOT NULL AND Director != ''
GROUP BY Director
ORDER BY total_movies DESC
LIMIT 1;

-- 4. Average rating per year
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
