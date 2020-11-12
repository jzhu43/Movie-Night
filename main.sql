-- -- CREATE TABLE Actor(
-- --     actorID varchar(50) primary key not null,
-- --     name varchar(50) not null,
-- --     dob date not null
-- -- );

-- -- CREATE TABLE Appears(
-- --     actorID varchar(50) primary key not null,
-- --     movieID varchar(50) not null,
-- --     role varchar(15) not null
-- -- );

-- -- CREATE TABLE Movie(
-- --     movieID varchar(50) primary key not null,
-- --     title varchar(40) not null,
-- --     year integer not null,
-- --     length float not null,
-- --     companyName varchar(40) not null,
-- --     director varchar(50) not null,
-- --     rating varchar(5) not null

-- -- );

-- -- CREATE TABLE Director(
-- --     dirID integer primary key not null,
-- --     dirName varchar(50) not null,
-- --     dob date not null
-- -- );

-- -- CREATE TABLE Genre(
-- --     movieID integer primary key not null,
-- --     genreType varchar(20) not null
-- -- );

-- -- CREATE TABLE Review(
-- --     movieID integer primary key not null,
-- --     imdb integer not null,
-- --     rottent integer not null
-- -- );

-- -- CREATE TABLE Company(
-- --     name varchar(40) primary key not null,
-- --     location varchar(80) not null
-- -- );

-- #1
SELECT DISTINCT d_name
FROM director
WHERE d_name LIKE '%Franco';

-- #2
SELECT count(g_genre)
FROM genre
WHERE g_genre LIKE 'DRAMA';

--#2.5
SELECT m_title, m_year, g_genre
FROM movies, genre
WHERE m_moveid = g_movieid
    AND g_genre LIKE 'DRAMA'
ORDER BY m_title ASC;

--#3
SELECT a_actorid, a_name, a_dob
FROM actor
WHERE a_name LIKE 'James%'
    AND a_dob LIKE '%1930';

--#4
SELECT m_title, m_year, m_length, r_imdb
FROM movies, review
WHERE movies.m_moveid = review.r_movieid
    AND review.r_imdb > 5.5
    AND m_length > 80
    AND m_length < 160
    AND m_year > 1950
    AND m_title LIKE 'The %'
ORDER BY m_year, r_imdb, m_length;
    
--#5
SELECT m_title, m_year, g_genre
FROM movies, genre
WHERE m_moveid = g_movieid
    AND g_genre LIKE 'COMEDY'
    AND m_year = 2001
ORDER BY m_title ASC;

--#6
SELECT m_title, m_year, a_name, app_role
FROM movies, actor, appears
WHERE m_moveid = app_miveid	
    AND a_actorid = app_actorid
GROUP BY m_title, app_role;

--#7
SELECT m_title, m_company, d_name
FROM movies, director, company
WHERE m_company = c_company
    AND d_name = m_director
GROUP BY d_name

--#8
SELECT m_title, m_year, a_name, app_role, g_genre, r_imdb, r_rottent
FROM movies, actor, appears, genre, review
WHERE m_moveid = app_miveid
    AND movies.m_moveid = review.r_movieid
    AND m_moveid = g_movieid
    AND a_actorid = app_actorid
    AND r_imdb > 6
    AND r_rottent > 5
GROUP BY m_title, app_role
ORDER BY m_year DESC, r_rottent ASC, r_imdb ASC;

--#9
SELECT m_title, g_genre
FROM movies, genre
WHERE m_moveid = g_movieid
ORDER BY g_genre ASC;

--#10
SELECT m_title, m_year, g_genre, m_length
FROM movies, genre
WHERE m_moveid = g_movieid
    AND g_genre LIKE 'ACTION'
    AND m_year = 2005
UNION 
SELECT m_title, m_year, g_genre, m_length
FROM movies, genre
WHERE m_moveid = g_movieid
    AND g_genre LIKE 'DRAMA'
    AND m_year = 2005
ORDER BY g_genre;

--#11
SELECT m_title, a_name, app_role, a_dob, c_company, d_name, g_genre, r_imdb
FROM actor, appears, company, director, genre, movies, review
WHERE m_moveid = app_miveid	
    AND movies.m_moveid = review.r_movieid
    AND m_moveid = g_movieid
    AND a_actorid = app_actorid
    AND m_company = c_company 
    AND d_name = m_director
GROUP BY m_title;

--#12
SELECT DISTINCT m_title, m_year
FROM appears, actor, movies
WHERE m_moveid = app_miveid	
    AND a_actorid = app_actorid
    AND app_role = 'actress'

--#12.5
SELECT count(*)
FROM (SELECT DISTINCT m_title
FROM appears, actor, movies
WHERE m_moveid = app_miveid	
    AND a_actorid = app_actorid
    AND app_role = 'actress') AS movie;

--#13

SELECT DISTINCT m_title, m_year
FROM appears, actor, movies
WHERE m_moveid = app_miveid	
    AND a_actorid = app_actorid
    AND app_role = 'actor';

--#14
SELECT DISTINCT c_company, c_location
FROM company, movies
WHERE m_title = 'Cleopatra'
    AND m_company = c_company 

--#15
SELECT m_title, m_moveid, d_name
FROM director, movies
WHERE d_name = m_director
    AND d_name = 'D.W. Griffith'
GROUP BY m_title;

--#16
SELECT a_actorid, a_name, c_company
FROM actor, movies, company, appears
WHERE m_moveid = app_miveid	
    AND a_actorid = app_actorid
    AND m_company = c_company 
    AND c_company = 'Touchstone Pictures'
GROUP BY a_name
ORDER BY a_name ASC;

--#17
SELECT m_title, a_name, m_director, c_company
FROM company, movies, director, actor, appears
WHERE m_moveid = app_miveid	
    AND a_actorid = app_actorid
    AND m_company = c_company 
    AND d_name = m_director
    AND c_company IN (SELECT c_company
                    FROM company
                    WHERE c_company LIKE '%Film%')
GROUP BY m_title, a_name;

--#18
SELECT distinct m_title, m_year, a_name, d_name
from director, movies, actor
where d_name = a_name
    and m_director = d_name
    and m_year < 1950
GROUP BY a_name;

--#19
SELECT m_moveid, m_title, c_company, g_genre
from genre, company, movies
where m_company = c_company
    and g_movieid = m_moveid
    and g_genre NOT IN (select g_genre
                        from genre
                        where g_genre LIKE 'Mystery')
GROUP BY c_company;

--#20
SELECT m_title, g_genre
from genre, movies, review
    where r_movieid = m_moveid
        and g_movieid = m_moveid
        and r_imdb > 6
        and r_rottent > 7
        and g_genre = (select g_genre
                        from genre
                        where  g_genre LIKE 'Romance')
Order by m_title ASC;


--# Inserting into a table and the query to show it's located in the table
INSERT INTO review VALUES ('tt0', '5.1', '5.4');
SELECT r_movieid, r_imdb, r_rottent
FROM review
WHERE r_movieid LIKE 'tt0';

INSERT INTO genre(g_movieid, g_genre) VALUES('tt0', 'Western')
select g_movieid, g_genre
from genre
where g_movieid LIKE 'tt0';

--# Deleting from a table with the specified conditions
DELETE FROM review where r_movieid LIKE 'tt0';

DELETE FROM genre where g_movieid LIKE 'tt0';

--# Updating an existing tuple in the table with the specified conditions
UPDATE genre SET g_genre = 'Drama' where g_movieid = 'tt0'
select g_movieid, g_genre
from genre
where g_movieid LIKE 'tt0';