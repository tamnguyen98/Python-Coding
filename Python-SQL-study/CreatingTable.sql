SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS genresRelation;
DROP TABLE IF EXISTS keywordsRelation;
DROP TABLE IF EXISTS productionCoRelation;
DROP TABLE IF EXISTS productionCountryRelation;
DROP TABLE IF EXISTS languagesRelation;
DROP TABLE IF EXISTS keywords;
DROP TABLE IF EXISTS productionCo;
DROP TABLE IF EXISTS productionCountry;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS languages;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE genres (
	id mediumint NOT NULL,
	info varchar(50),
	PRIMARY KEY(id)
);

CREATE TABLE keywords (
	id mediumint NOT NULL,
	info varchar(100),
	PRIMARY KEY(id)
);

CREATE TABLE productionCo (
	id mediumint NOT NULL,
	info varchar(100),
	PRIMARY KEY(id)
);

CREATE TABLE productionCountry (
	sName varchar(2),
	lName varchar(60), 
	PRIMARY KEY(sName)
);

CREATE TABLE languages (
	sName varchar(2),
	lName varchar(20),
	PRIMARY KEY(sName)
);


CREATE TABLE movies (
	budget bigint,
	homepage varchar(400),
	id  mediumint NOT NULL,
	orig_language varchar(2),
	title varchar(100),
	overview varchar(1000),
	popularity double,
	release_date varchar(20),
	revenue bigint,
	runtime smallint,
	movieStatus varchar(25),
	tagline varchar(600),
	vote_avg float,
	vote_count mediumint,
	PRIMARY KEY(id)
);

CREATE TABLE genresRelation (
	movieId mediumint NOT NULL,
	itemID mediumint,
	PRIMARY KEY (movieId, itemID),
	FOREIGN KEY (movieId) references movies(id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (itemID) references genres(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE keywordsRelation (
	movieId mediumint NOT NULL,
	itemID mediumint  NOT NULL,
	PRIMARY KEY (movieId, itemID),
	FOREIGN KEY (movieId) references movies(id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (itemID) references keywords(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE productionCoRelation (
	movieId mediumint NOT NULL,
	itemID mediumint NOT NULL,
	PRIMARY KEY (movieId, itemID),
	FOREIGN KEY (movieId) references movies(id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (itemID) references productionCo(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE productionCountryRelation (
	movieId mediumint NOT NULL,
	abbrev varchar(2)  NOT NULL,
	PRIMARY KEY (movieId, abbrev),
	FOREIGN KEY (movieId) references movies(id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (abbrev) references productionCountry(sName) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE languagesRelation (
	movieId mediumint NOT NULL,
	abbrev varchar(2)  NOT NULL,
	PRIMARY KEY (movieId, abbrev),
	FOREIGN KEY (movieId) references movies(id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (abbrev) references languages(sName) ON UPDATE CASCADE ON DELETE CASCADE
);