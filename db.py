from flask_mongoengine import  MongoEngine

db=MongoEngine()

def intialize_db(app):
    db.init_app(app)