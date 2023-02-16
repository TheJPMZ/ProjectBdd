import pymongo

def connecta():
    
    try:
        client = pymongo.MongoClient("mongodb+srv://jpmz:jpmz@cluster0.vfoeymk.mongodb.net/?retryWrites=true&w=majority")
    except:
        raise Exception("Could not connect to MongoDB")

    db = client["sample_mflix"]

    return db
