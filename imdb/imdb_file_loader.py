#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'vamshi'

from hashlib import md5
from pymongo import MongoClient
from imdb_file_parser import ImdbParser

class ImdbMovieDataLoader(object):
    def __init__(self, outFolder):
        self.imdbparser = ImdbParser(outFolder)
        self.movies = {}

    def __update_movies_dict_with_titles(self):
        titles = self.imdbparser.generate_movie_titles()
        for tl in titles:
            t = md5(tl.encode('utf-8')).hexdigest()
            self.movies.setdefault(t,{"title" : tl, "movieid":t})
            self.movies[t]["year"] = self.imdbparser.parse_title(tl)["year"]
            self.movies[t]["kind"] = self.imdbparser.parse_title(tl)["kind"]

    def __update_movies_dict_with_genres(self):
        genres = self.imdbparser.generate_genres()
        for tl,g in genres:
            t = md5(tl.encode('utf-8')).hexdigest()
            self.movies.setdefault(t,{"title":tl, "movieid":t})
            self.movies[t].setdefault("genres",[]).append(g)

    def __update_movies_dict_with_ratings(self):
        ratings = self.imdbparser.generate_ratings()
        for tl,r in ratings:
            t = md5(tl.encode('utf-8')).hexdigest()
            self.movies.setdefault(t,{"title":tl, "movieid":t})
            self.movies[t]["ratings"] = r

    def __update_movies_dict_with_languages(self):
        languages = self.imdbparser.generate_languages()
        for tl,l in languages:
            t = md5(tl.encode('utf-8')).hexdigest()
            self.movies.setdefault(t,{"title":tl, "movieid":t})
            self.movies[t].setdefault("language", []).append(l)

    def __update_movies_dict_with_running_times(self):
        rtimes = self.imdbparser.generate_running_times()
        for tl,rt in rtimes:
            t = md5(tl.encode('utf-8')).hexdigest()
            self.movies.setdefault(t,{"title":tl, "movieid":t})
            self.movies[t]["running-time"] = rt

    def __update_movies_dict_with_actors(self):
        actors = self.imdbparser.generate_actors()
        for tl,a,s,r,b in actors:
            t = md5(tl.encode('utf-8')).hexdigest()
            self.movies.setdefault(t,{"title":tl, "moivieid":t})
            #self.movies[t].setdefault("actors",[]).append({"name":a,"sex":s,"role":r,"bill_pos":b})
            self.movies[t].setdefault("actors",[]).append(a)

    def __update_movies_dict_with_directors(self):
        directors = self.imdbparser.generate_directors()
        for tl,d in directors:
            t = md5(tl.encode('utf-8')).hexdigest()
            self.movies.setdefault(t,{"title":tl, "movieid":t})
            self.movies[t].setdefault("directors",[]).append(d)

    def __update_movies_dict(self):
        try:
            self.__update_movies_dict_with_actors()
        except: pass
        try:
            self.__update_movies_dict_with_directors()
        except: pass
        try:
            self.__update_movies_dict_with_genres()
        except: pass
        try:
            self.__update_movies_dict_with_languages()
        except: pass
        try:
            self.__update_movies_dict_with_ratings()
        except: pass
        try:
            self.__update_movies_dict_with_running_times()
        except: pass
        try:
            self.__update_movies_dict_with_titles()
        except: pass


    def load_mongodb_bulk(self, host, port, db_name, coll_name):
        if not self.movies:
            self.__update_movies_dict()
        client = MongoClient(host, port)
        db = client[db_name]
        movies_coll = db[coll_name]
        it = iter(self.movies.itervalues())
        n = len(self.movies)
        chunksize = 1000
        q = int(n / chunksize)
        r = n % chunksize
        l = []
        for i in range(r):
            l.append(next(it))
        movies_coll.insert(l)
        for i in range(q):
            l = []
            for j in range(chunksize):
                l.append(next(it))
            movies_coll.insert(l)

