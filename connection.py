import pymongo

def connecta():
    
    try:
        client = pymongo.MongoClient("mongodb+srv://admin:NmtDOXhkfoQo7pFI@atlascluster.mgohz2e.mongodb.net/?retryWrites=true&w=majority")
    except:
        raise Exception("Could not connect to MongoDB")

    db = client["test"]

    return db
