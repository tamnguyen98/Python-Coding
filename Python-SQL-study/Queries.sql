SELECT avg(budget) as Avg_Budget FROM movies  LIMIT 5;

SELECT movies.title, productionco.info as ProductionCo 
FROM movies 
	INNER JOIN productioncountryrelation 
		ON movies.id = productioncountryrelation.movieId 
	INNER JOIN productioncorelation
		on movies.id = productioncorelation.movieId
	INNER JOIN productionco
		ON productionco.id = productioncorelation.itemID
WHERE productioncountryrelation.abbrev='US'
LIMIT 5;

SELECT title, revenue FROM movies ORDER BY revenue DESC LIMIT 5;

SELECT DISTINCT t1.title as Movie, genres.info as Genre
from (
	SELECT m.ID, m.title
    FROM
		(SELECT distinct movies.title, genres.info as Genre, movies.id as ID
		FROM movies
			left outer JOIN genresrelation
				ON movies.id = genresrelation.movieId
			left outer JOIN genres
				ON genresrelation.itemId = genres.id
		WHERE genres.info = 'Mystery') as m
    INNER JOIN
		(SELECT distinct movies.title, genres.info as Genre, movies.id as ID
		FROM movies
			left outer JOIN genresrelation
				ON movies.id = genresrelation.movieId
			left outer JOIN genres
				ON genresrelation.itemId = genres.id
		WHERE genres.info = 'Science Fiction') as f
    ON m.ID = f.ID
) AS t1 INNER JOIN genresrelation
		on t1.ID = genresrelation.movieId
INNER JOIN genres
	on genresrelation.itemID = genres.id
LIMIT 5;

SELECT movies.title, movies.popularity
FROM movies
WHERE popularity > (SELECT avg(popularity) FROM movies) LIMIT 5;