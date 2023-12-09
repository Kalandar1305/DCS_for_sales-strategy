import pymongo

try:
    client = pymongo.MongoClient('mongodb://172.17.0.1:27017')
    db = client['project']
    print('MongoDB connection successful!')

except pymongo.errors.ConnectionFailure as e:
    print('MongoDB connection failed: %s' % e)