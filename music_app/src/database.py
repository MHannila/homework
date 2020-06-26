HOST = 'mongodb'
PORT = 27017
USER = 'mongoadmin'
PASSWORD = 'mongopass'


def client():
    import pymongo

    return pymongo.MongoClient(f'mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/')
