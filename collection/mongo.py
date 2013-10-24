import pymongo

import conf

db = pymongo.MongoClient(conf.MONGODB_CONNECTION_STRING)[conf.MONGODB_DATABASE]