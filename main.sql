CREATE TABLE Actor(
    actorID varchar(50) primary key not null,
    name varchar(50) not null,
    dob date not null
);

CREATE TABLE Appears(
    actorID varchar(50) primary key not null,
    movieID varchar(50) not null,
    role varchar(15) not null
);

CREATE TABLE Movie(
    movieID varchar(50) primary key not null,
    title varchar(40) not null,
    year integer not null,
    length float not null,
    companyName varchar(40) not null,
    director varchar(50) not null,
    rating varchar(5) not null

);

CREATE TABLE Director(
    dirID integer primary key not null,
    dirName varchar(50) not null,
    dob date not null
);

CREATE TABLE Genre(
    movieID integer primary key not null,
    genreType varchar(20) not null
);

CREATE TABLE Review(
    movieID integer primary key not null,
    imdb integer not null,
    rottent integer not null
);

CREATE TABLE Company(
    name varchar(40) primary key not null,
    location varchar(80) not null
);

