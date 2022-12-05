#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This program creates and fill a data base with all the cities in the world.

Two tables will be created: 'countries' and 'cities'.

Each line in the input file from countries should have the following format:

    CODE,"Country Name"

where CODE is a string of two characters.

The lines of cities file should have the following format:

    CODE,Name no accents,Name with accents,...

where CODE is the country two characters code and ... means other irrelevant
information.

The countries and cities files were downloaded, respectively, from

    http://www.maxmind.com/app/iso3166
    http://www.maxmind.com/download/worldcities/worldcitiespop.txt.gz

For more information visit:

    http://www.maxmind.com/app/worldcities

The names of the cities are the standard names approved by the United States
Board on Geographic Names and mantained by the National Geospatial-Intelligence
Agency.

The encoding of the input files are ISO-8859-1. We will save only UNICODE
strings in the data base. This way you will have no encoding problems because
you can choose whatever encoding you want in the output 
(UTF-8 is commonly used).

The program was tested successfully with PostgreSQL and SQLite3, but it should 
work with all data bases supported by SQLAlchemy package. The final data base
will ocupy 86mb in disk with SQLite and aproximatelly the same ammount with
PostgreSQL. This program uses 20mb of RAM memory.
Also, there is no redundant data in the tables.


Type --help to see how to use the program.


author: Guilherme Starvaggi França <guifranca@gmail.com>
date: 2010-09-05

"""

import re, sys, optparse, time
import sqlalchemy as sa

# absolute path to sqlite file db
sqlite_path = '/home/guisf/prog/andy_cities_world/world_cities.db'

# string to connect to data base
db = "sqlite:///%s" % sqlite_path

# encoding used in the text files
encoding = 'iso-8859-1'

# read file in chunks to not overflow memory (20mb default)
bytes = 20*(2**20)

country_patt = re.compile(r'(\w{2}),"(.+)"\s?')
engine = sa.create_engine(db, echo=False, encoding='utf-8', 
                          convert_unicode=True)
metadata = sa.MetaData(bind=engine)

countries = sa.Table('countries', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('code', sa.Unicode(2)),
    sa.Column('name', sa.Unicode(50)),
)

cities = sa.Table('cities', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('country_id', sa.Integer, sa.ForeignKey('countries.id')),
    sa.Column('na_name', sa.Unicode(90)), # non accented name
    sa.Column('name', sa.Unicode(90)),
)

tmpcities = sa.Table('tmpcities', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('country_id', sa.Integer, sa.ForeignKey('countries.id')),
    sa.Column('na_name', sa.Unicode(90)), # non accented name
    sa.Column('name', sa.Unicode(90)),
)

def timed(func):
    """Execute the function and measure how time it takes."""
    def wrapper(*args, **kwargs):
        b = time.time()
        result = func(*args, **kwargs)
        e = time.time()
        print("<%s> took %fs to execute." % (func.__name__, e-b))
        return result
    return wrapper

def biggest_city_len(file):
    """Return len of biggest city."""
    max = 0
    fcity = ''
    for line in open(file):
        code, trash, city = line.split(',')[:3]
        n = len(city)
        if n > max:
            max = n
            fcity = city
    return max, fcity

def biggest_country_len(file):
    """Return len of biggest country."""
    max = 0
    fcountry = ''
    for line in open(file):
        code, name = country_patt.match(line).groups()
        n = len(name)
        if n > max:
            max = n
            fcountry = name
    return max, fcountry

@timed
def fill_countries(file):
    """The file should have all lines with the following format:
    
    CODE,"Country Name"

    where CODE is two chars. This function will drop and recriate cities
    and countries tables.
    
    """
    try:
        f = open(file)
    except:
        print("File '%s' does not exist. Aborting." % file)
        sys.exit(1)
    data = []
    for line in f:
        try:
            code, name = country_patt.match(line).groups()
        except:
            pass
        name = name.decode(encoding)
        code = code.decode(encoding).lower()
        data.append({'code': code, 'name': name})
    countries.drop(checkfirst=True)
    countries.create()
    conn = engine.connect()
    conn.execute(countries.insert(), data)
    conn.close()
    f.close()

@timed
def fill_cities(file):
    """The file should have all lines in the format:
    
    CODE,No accents name,Accented name,other data ...
    
    CODE is the country code. The table will be droped and recriated to
    prevent duplicate data.

    """
    try:
        conn = engine.connect()
        r = conn.execute(sa.sql.select([countries])).fetchall()
        assert len(r) > 0
        cts = dict([(c[1], c[0]) for c in r])
        tmpcities.drop(checkfirst=True)
        tmpcities.create()
    except:
        print("It seems that you haven't inserted countries in the data base.")
        print("See the -1 option to do that.")
        print("Aborting!")
        sys.exit(1)
    finally:
        conn.close()
    try:
        f = open(file)
    except:
        print("File '%s' does not exist. Aborting!" % file)
        sys.exit(1)
    
    while True:
        data = []
        lines = f.readlines(bytes)
        conn = engine.connect()
        if not lines:
            break
        for line in lines:
            code, na_name, name = line.split(',')[:3]
            name = name.decode(encoding)
            na_name = na_name.decode(encoding)
            try:
                id = cts[code.lower()]
            except:
                continue
            data.append({'country_id': id, 'na_name': na_name, 'name': name})
        conn.execute(tmpcities.insert(), data)
        conn.close()
    f.close()

@timed
def del_duplicates():
    """Eliminate duplicate cities in tmpcities and create cities.
    tmpcities will be deleted.
    
    """
    cities.drop(checkfirst=True)
    cities.create()
    allcountries = countries.select().execute().fetchall()
    for country in allcountries:
        buffer = {}
        data = []
        allcities = tmpcities.select(tmpcities.c.country_id==country[0]).\
                                                        execute().fetchall()
        for city in allcities:
            country_city = u'%i-%s' % (city[1], city[2])
            if country_city not in buffer:
                data.append({'country_id': city[1], 'na_name': city[2], 
                             'name': city[3]})
                buffer[country_city] = 1
        if data:
            cities.insert().execute(data)
    tmpcities.drop()


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-1", "--countries", dest="country_file",
                      help="Fill data base with countries contained in FILE. "\
                      "The cities table will be cleaned if it already exists.",
                      metavar="FILE")
    parser.add_option("-2", "--cities", dest="city_file",
                      help="Fill data base with cities contained in FILE."\
                      "The countries table must already exist. "\
                      "The cities table will be cleaned if it already exists.",
                      metavar="FILE")
    parser.add_option("-l", "--city_length", dest="city_length", 
                      help="Tell the max number of characters of the cities "\
                           "contained in FILE", metavar="FILE")
    parser.add_option("-n", "--country_length", dest="country_length", 
                      help="Tell the max number of characters of the "\
                           "countries contained in FILE", metavar="FILE")
    parser.add_option("-r", "--readme", dest="readme", action="store_true",
                      help="Readme", default=False)
    options, args = parser.parse_args()

    if options.country_file:
        print("Filling countries table.")
        fill_countries(options.country_file)
        print("Done!")
    elif options.city_file:
        print("Filling cities table.")
        try:
            fill_cities(options.city_file)
            del_duplicates()
            print("Done!")
        except Exception, e:
            raise
            print('Error:')
            print(e[:500])
            sys.exit(1)
    elif options.city_length:
        print(biggest_city_len(options.city_length))
    elif options.country_length:
        print(biggest_country_len(options.country_length))
    elif options.readme:
        print(__doc__)

