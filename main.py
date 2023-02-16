import pymongo
from connection import connecta

db = connecta()

USERS = db["users"]
MOVIES = db["movies"]
COMMENTS = db["comments"]
SESSIONS = db["sessions"]

# CRUD
def create_user():
    user = {"name": "", "email": "", "password":""}
    user.name = input("Enter your name: ")
    user.email = input("Enter your email: ")
    user.password = input("Enter your password: ")
    USERS.insert_one(user)

def read_users():
    users = USERS.find()
    for user in users:
        print(user)

def delete_user():
    username = input("Enter the username you want to delete: ")
    USERS.delete_one({"name": username})
    
def update_user():
    username = input("Enter the username you want to update: ")
    newname = input("Enter the new username: ")
    USERS.update_one({"name": username}, {"$set": {"name": newname}})

# Ordenar
def users_sorted():
    users = USERS.find().sort("name")
    for user in users:
        print(user)

# Proyeccinón y filtrado
def proyect_movies():
    
    regex = input("Enter a movie title: (Can be just 1 word)" )
    
    result = MOVIES.aggregate([
    {
        '$match': {
            'title': {
                '$regex': regex
            }
        }
    },{'$project': {'title':1}}])
    print(list(result))

# Usar documentos embeded
def comments_in_movie():
    
    movie = input("Enter a movie title: ")
        
    result = MOVIES.aggregate([
    {
        '$match': {
            'title': movie
        }
    },{'$lookup': {
        'from': 'comments',
        'localField': '_id',
        'foreignField': 'movie_id',
        'as': 'comments'
    }}])
    print(list(result))

# Ordenar y limitar
def worse_movies():
    
    result = MOVIES.aggregate([
    {
        '$sort': {
            'imdb.rating': 1
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



