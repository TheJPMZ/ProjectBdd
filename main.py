import pymongo
from connection import connecta

db = connecta()

VIDEOS = db["documennts"]
USERS = db["users"]


def read_users():
    users = VIDEOS.find()
    for user in users:
        print(user)

# Proyeccinón y filtrado
def proyect_movies():
    
    regex = input("Enter a movie title: (Can be just 1 word)" )
    
    result = VIDEOS.aggregate([
    {
        '$match': {
            'title': {
                '$regex': regex
            }
        }
    },{'$project': {'title':1,'_id':0}}])
    for x in result:
        print(x["title"])

# Usar documentos
def comments_in_video():
    
    movie = input("Enter a movie title: ")
    comment = input("Enter a comment: ")
    
    result = VIDEOS.update_one(
        {"title": movie},
        {"$push": {"comments": comment}}
    )

    print(result)

# Ordenar y limitar
def worse_movies():
    
    result = VIDEOS.aggregate([
    {
        '$sort': {
            'reactions.dislikes': -1,
        }
    },{'$limit': 10}])
    print(list(result))
   
   
# Arrays y agregaciones complejas 
def actors_movies():
    result = MOVIES.aggregate([
    {
        '$unwind': {
            'path': '$cast', 
            'includeArrayIndex': 'actor'
        }
    }, {
        '$group': {
            '_id': '$cast', 
            'movies': {
                '$count': {}
            }
        }
    }, {
        '$sort': {
            'movies': -1
        }
    }, {
        '$limit': 5
    }
    ])
    print(list(result))
  
# BUlk write
print(SESSIONS.count_documents({}))
  
sessions = [{ "user_id": 1, "jwt": "pata" },
            { "user_id": 2, "jwt": "peta" },
            { "user_id": 3, "jwt": "pita" },
            { "user_id": 4, "jwt": "pota" },
            { "user_id": 5, "jwt": "Maria Antonieta" }]

bulk = []
for x in sessions:
    bulk.append(pymongo.InsertOne(x))
    
SESSIONS.bulk_write(bulk)

print(SESSIONS.count_documents({}))


