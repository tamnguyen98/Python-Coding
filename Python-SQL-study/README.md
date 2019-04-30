# Python SQL study

# About
This program takes a database (tmdb_5000_movies.csv) and parse all the tuples to be added to a MYSQL database via python.

### Features

- Deals with csv parsing
- Using MySQL in python
- Connecting to MySQL database
- Querying data

### How to use
Run the following commands
```

py Main.py user pass <query #>

```

Where py is the your python execution, user and pass is your database login, and query number being 1-5 displaying the following:
1: Average budget value of all movies combined
2: List of all movies (and its production co.) that was produced in the US
3: Top 5 movies that made the most revenue
4: List of movies that contains both genre of Science Fiction and Mystery
5: List of all movies that have popularities higher than the average popularity of all the movies combined

###NOTICE
If no query number are given, the program will print all query in the same order!

### WARING
Make sure to change the 'schemaName' in Main.py to match your SQL database's schema!

#### Example
```

>py Main.py root 123456

# Query 1
(Decimal('29045039.8753'),)

# Query 2
('Four Rooms', 'Miramax Films')
('Star Wars', 'Lucasfilm')
('Finding Nemo', 'Pixar Animation Studios')
('Forrest Gump', 'Paramount Pictures')
('American Beauty', 'DreamWorks SKG')

# Query 3
('Avatar', 2787965087)
('Titanic', 1845034188)
('The Avengers', 1519557910)
('Jurassic World', 1513528810)
('Furious 7', 1506249360)

# Query 4 (empty)

# Query 5
('Four Rooms', 22.87623)
('Star Wars', 126.393695)
('Finding Nemo', 85.688789)
('Forrest Gump', 138.133331)
('American Beauty', 80.878605)

```