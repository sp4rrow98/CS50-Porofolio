SELECT movies.title FROM people
JOIN stars ON stars.person_id = people.id
JOIN movies ON stars.movie_id = movies.id
JOIN ratings ON ratings.movie_id = movies.id
WHERE people.name = "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5