from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import mongoengine as me
import sys

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
  'db': 'flask_project',
  'host': 'localhost',
  'port': 27017
}

db = MongoEngine()
db.init_app(app)
CORS(app)

class Bookmark(me.Document):
  title = me.StringField(required=True)
  url = me.StringField()
  tags = me.ListField(me.StringField())
  completed = me.BooleanField()
  editing = me.BooleanField()

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
  if request.method == 'GET':
    bookmarks = Bookmark.objects
    return jsonify(bookmarks)

  if request.method == 'POST':
    body = request.get_json()
    bookmark = Bookmark(**body).save()
    title = bookmark.title
    url = bookmark.url
    id = bookmark.id
    known_topics = ["python", "flask", "mongo"]

    for topic in known_topics:
      if topic in title:
        Bookmark.objects(id=id).update_one(push__tags=topic)
        print("title match")

      if topic in url:
        Bookmark.objects(id=id).update_one(push__tags=topic)
        print("url match")

  return {'title': str(title)}, 200
