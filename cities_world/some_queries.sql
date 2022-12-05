/* drop tables */

DROP TABLE countries;
DROP TABLE cities;


/* creating tables */

CREATE TABLE countries (
    id INTEGER NOT NULL, 
    code VARCHAR(2), 
    name VARCHAR(50), 
    PRIMARY KEY (id)
)

CREATE TABLE cities (
        id INTEGER NOT NULL, 
        country_id INTEGER, 
        na_name VARCHAR(90), 
        name VARCHAR(90), 
        PRIMARY KEY (id), 
        FOREIGN KEY(country_id) REFERENCES countries (id)
)


/* select country with some name */

SELECT * FROM countries WHERE name LIKE 'serbia';
SELECT * FROM countries WHERE name LIKE '%erbia%';


/* select some city, the pattern must be non accented */

SELECT * FROM cities WHERE na_name LIKE 'sao paulo';
SELECT * FROM cities WHERE na_name LIKE '%sao paulo%';


/* select cities form a specific country */

SELECT cities.id, cities.na_name, cities.name FROM cities, countries WHERE cities.country_id=countries.id AND countries.name LIKE 'brazil';

SELECT cities.id, cities.na_name, cities.name FROM cities, countries WHERE cities.country_id=countries.id AND countries.code='us';


