__author__ = 'vamshi'
from pymongo import ASCENDING, DESCENDING, TEXT, MongoClient

HOST = 'localhost'
PORT = 27017
DB_NAME = 'imdb'
COLL_NAME = 'movies'

client = MongoClient(HOST, PORT)
db = client[DB_NAME]
movies_coll = db[COLL_NAME]

def create_indices():
    movies_coll.create_index([("ratings", DESCENDING)])
    movies_coll.create_index("language")
    movies_coll.create_index([("year", DESCENDING)])
    movies_coll.create_index([("kind", DESCENDING)])
    movies_coll.create_index([("running-time", DESCENDING)])
    movies_coll.create_index([("$**",TEXT)],default_language="en",language_override= "en")
    movies_coll.create_index([("ratings", DESCENDING), ("language",DESCENDING), ("year", DESCENDING)])

if __name__ == "__main__":
    # create_indices()
    # print movies_coll.count()
    # print movies_coll.find({"ratings":{"$exists":True}}).count()
    # print movies_coll.find({"actors":{"$exists":True}}).count()
    # print movies_coll.find({"genres":{"$exists":True}}).count()
    # print movies_coll.find({"directors":{"$exists":True}}).count()
    # print movies_coll.find({"title":{"$exists":True}}).count()
    # print movies_coll.find({"language":{"$exists":True}}).count()
    # print movies_coll.find({"running-time":{"$exists":True}}).count()
    # print movies_coll.find({"kind":{"$exists":True}}).count()
    # print movies_coll.find({"year":{"$exists":True}}).count()

    #for mov in movies_coll.find({"$and":[{"language":"Telugu"},{"kind":"mo"},{"year":2014}]}).sort("ratings", DESCENDING).limit(25):
    #    print mov["title"], mov.get("ratings",None)

    #for year in range(1931,2016):
    #    for mov in movies_coll.find({"$and":[{"language":"Telugu"},{"kind":"mo"},{"year":year}]}).sort("ratings", DESCENDING).limit(50):
    #        print mov["year"], mov["title"], mov.get("ratings",None)

    #for mov in movies_coll.find({"$and":[{"actors":"Khan, Aamir (I)"},{"kind":"mo"},{"language":"Hindi"}]}).sort("ratings",DESCENDING):
    #    print mov["title"], mov.get("ratings",None)

    #for mov in movies_coll.find({"$and":[{"actors":"Khan, Aamir (I)"},{"kind":"mo"},{"language":"Hindi"}]}).sort("ratings",DESCENDING):
    #    print mov["title"], mov.get("ratings",None)

    #for mov in movies_coll.find({"$and":[{"actors":"Khan, Shah Rukh (I)"},{"kind":"mo"},{"language":"Hindi"}]}).sort("ratings",DESCENDING):
    #    print mov["title"], mov.get("ratings",None)

    #for mov in movies_coll.find({"$and":[{"$text":{"$search":"Jandhyala"}},{"kind":"mo"},{"language":"Telugu"}]}).sort("ratings",DESCENDING):
    #    print mov["title"], mov.get("ratings",None), mov.get("actors",None)

    #for mov in movies_coll.find({"$and":[{"directors":"Jandhyala"},{"kind":"mo"},{"language":"Telugu"}]}).sort("ratings",DESCENDING):
    #    print mov["title"], mov.get("ratings",None)


    #for i, mov in enumerate(movies_coll.find({"$and":[{"actors":"Brahmanandam"},{"kind":"mo"},{"language":"Telugu"}]}).sort("ratings",DESCENDING)):
    #    print i, mov["title"], mov.get("ratings",None), mov.get("actors",None)

    for i, mov in enumerate(movies_coll.find({"$and":[{"actors":"Chiranjeevi (I)"},{"kind":"mo"},{"language":"Telugu"}]}).sort("ratings",DESCENDING)):
        print i, mov["title"], mov.get("ratings",None)