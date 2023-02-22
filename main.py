import pymongo
from flask import Flask, render_template, request,Response,jsonify, redirect,url_for
from connection import connecta

db = connecta()

app = Flask(__name__)

VIDEOS = db["documennts"]
USERS = db["users"]

@app.route('/')
def home():
    return render_template('index.html')


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
    result = VIDEOS.aggregate([
    {
        '$unwind': {
            'path': '$comments', 
            'includeArrayIndex': 'string'
        }
    }, {
        '$group': {
            '_id': '$comments', 
            'videos': {
                '$count': {}
            }
        }
    }, {
        '$sort': {
            'videos': -1
        }
    }, {
        '$limit': 10
    }, {
        '$project': {
            'Comment': '$_id', 
            'Count': '$videos', 
            '_id': 0
        }
    }
    ])
    print(list(result))
  
# BUlk write

def bulk_write():
    print(VIDEOS.count_documents({}))
  
    sessions = [
        {   
            "author": "Mike",
            "title": "My first videoblog",
            "duration": 10,
            "reactions": {
                "likes": 10,
                "dislikes": 2
            },
            "iframe": "https://www.youtube.com/embed/5Q672eeMCMs",
            "description": "This is my first video",
            "comments": ["Hate it", "I like it", "Nice video"]
        },
        {
            "author": "MoistCr1TiKaL",
            "title": "Rating markiplier's onlyfans",
            "duration": 10,
            "reactions": {
                "likes": 10000,
                "dislikes": 500
            },
            "iframe": "https://www.youtube.com/embed/JlLUp8I7qOo",
            "description": "Hot take",
            "comments": ["Wow", "What a video", "I like it"]
        },
        {
            "author": "IGN",
            "title": "Top 10 games of 2020",
            "duration": 11,
            "reactions": {
                "likes": 1000,
                "dislikes": 1000,
            },
            "iframe": "https://www.youtube.com/embed/nfbz1KuLXTc",
            "description": "Top 10 games of 2020",
            "comments": ["Nice", "Good video", "I like it"]
        }
    ]

    bulk = []
    for x in sessions:
        bulk.append(pymongo.InsertOne(x))
        
    VIDEOS.bulk_write(bulk)


    print(VIDEOS.count_documents({}))
    
    
if __name__ == '__main__':
    app.run(debug=True, port=3400)