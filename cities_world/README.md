# cities_world
Create a database of all the cities in the world.
This directory contains a program and text files used to generate a database
of all cities of the world with its respective country.


DEPENDENCIES
------------

> python 2.5
> python-sqlalchemy 0.5.8

Probably you should have python installed already, type `python -V` to see
what version you have. If it is lower than 2.5 you should upgrade:

[python](http://www.python.org/download/mac/)

You should also install SQLAlchemy:

[sqlalchemy](http://www.sqlalchemy.org)

If you need some help in doing this, tell me and I will help you.


FILES
-----

countries.txt: contains the list of countries that you will use

cities_1mb: it is a list of cities with only 1mb to test the
program, if you want, before running the whole 124mb list of cities.

some_queries.sql: contains some SQL queries that I thought relevant for you.

worldcities.py: the program to insert data. Type --help to see the options.


INSTRUCTIONS
------------

(1) Download the repositories of cities into this directory.

    wget http://www.maxmind.com/download/worldcities/worldcitiespop.txt.gz
    gzip -d worldcitiespop.txt.gz 


(2) The country 'Zaire' does not exist anymore, so remove bad entries:

    sed '/^zr/d' worldcitiespop.txt > all_cities.txt


(3) Open the file 'worldcities.py' and in line 57 alter the variable
'sqlite_path' to your data base file:

    # absolute path to sqlite file db
    sqlite_path = '/home/guisf/prog/andy_cities_world/world_cities.db'


(4) Insert countries (the countries.txt file is already there):

    ./worldcities.py -1 countries.txt


(5) Insert cities:

    ./worldcities.py -2 all_cities.txt

this last command can take about 7 minutes to execute.
