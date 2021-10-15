from flask import Flask, request, jsonify
from functools import wraps

from flask.helpers import make_response
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# jwt requirements
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = '5941616246dce89d94975a7c215692f40cda842a'
jwt = JWTManager(app) # jwtoken object
db = SQLAlchemy(app)
CORS(app)

class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))



book_post_args = reqparse.RequestParser()
book_post_args.add_argument("title", type=str, help="Title is required!", required=True)
book_post_args.add_argument("author", type=str, help="author is required!", required=True)

book_update_args = reqparse.RequestParser()
book_update_args.add_argument("title", type=str)
book_update_args.add_argument("author", type=str)

resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "author": fields.String
}


# JWT auth decorator
def admin(f):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return f(*args, **kwargs)
            else:
                return jsonify(message="Admins only!"), 403

        return decorator
    return wrapper


# login resource
class LoginAdmin(Resource):
    def post(self):
        '''generates the JWT token'''
        access_token = create_access_token("admin_user", additional_claims={"is_administrator": True})
        return jsonify(access_token=access_token)


class BookList(Resource):
    decorators = [admin] # adds the admin decorator

    def get(self):
        '''returns all books in the database'''
        books = BookModel.query.all()
        allBooks = {}
        for book in books:
            allBooks[book.id] = {"title": book.title, "author": book.author}
        return allBooks


class BookId(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        '''returns book by id '''
        book = BookModel.query.filter_by(id=book_id).first()
        if not book:
            abort(404, message="No book found with that id!")
        return book

    @marshal_with(resource_fields)
    def post(self, book_id):
        '''adds book by ID'''
        args = book_post_args.parse_args()
        book = BookModel.query.filter_by(id=book_id).first()
        if book:
            abort(409)
        
        newBook = BookModel(id=book_id, title=args["title"], author=args["author"])
        db.session.add(newBook)
        db.session.commit()
        return newBook, 201

    @marshal_with(resource_fields)
    def put(self, book_id):
        '''updates a book using its id'''
        args = book_update_args.parse_args()
        book = BookModel.query.filter_by(id=book_id).first()
        if not book:
            abort(404, message="No book found.")
        if args['title']:
            book.title = args["title"]
        if args["author"]:
            book.author = args["author"]
        db.session.commit()
        return book

    def delete(self, book_id):
        '''deletes book frm db with the provided id'''
        book = BookModel.query.filter_by(id=book_id).first()
        db.session.delete(book)
        return "Book deleted", 204


api.add_resource(BookList, "/bookapi/books") # gets all the books in the db.
api.add_resource(LoginAdmin, '/bookapi/login')
api.add_resource(BookId, "/bookapi/books/<int:book_id>") # use this to get/post a book
    
if __name__ == '__main__':
    app.run(debug=True)