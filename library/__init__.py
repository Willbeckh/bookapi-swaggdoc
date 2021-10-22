from flask import Flask
from config import Config
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

from library import models, resources
from library.resources import BookId, BookList, Signup, Login

api = Api(app)

# resource endpoints
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
# api.add_resource(AllUsers, '/users')
api.add_resource(BookList, "/bookapi/books") # gets all the books in the db.
api.add_resource(BookId, "/bookapi/books/<int:book_id>") # use this to get/post a book