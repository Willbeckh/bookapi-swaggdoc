from flask import request, jsonify
from flask.helpers import make_response
from flask_restful import Resource, abort, reqparse, fields, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
import jwt
from library import db, app
from library.models import BookModel, Users, token_required


# data parsing
book_post_args = reqparse.RequestParser()
book_post_args.add_argument("title", type=str, help="Title is required!", required=True)
book_post_args.add_argument("author", type=str, help="author is required!", required=True)

book_update_args = reqparse.RequestParser()
book_update_args.add_argument("title", type=str)
book_update_args.add_argument("author", type=str)

# data for user
user_post_data = reqparse.RequestParser()
user_post_data.add_argument("username", type=str, help="Username rqeuired!", required=True)
user_post_data.add_argument("password", type=str, help="Password required!", required=True)

# serializing db data to py objs(dict)
resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "author": fields.String
}

# user data format
user_fields = {
    "username": fields.String,
    "password": fields.String
}

# register route
class Signup(Resource):
    def post(self):
        data = user_post_data.parse_args()
        hashed_password = generate_password_hash(data['password'], method='sha256')

        user = Users.query.filter_by(username=data['username']).first()
        if not user:
            new_user = Users(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, admin=False)
            db.session.add(new_user)
            db.session.commit()
        return f"User:<{new_user.username}> registered successfully!", 201

# user login route
class Login(Resource):
    def post(self):
        auth_data = request.get_json()
        if not auth_data or not auth_data.get('username') or not auth_data.get('password'):
            abort(401, message="Could not verify user data!")
        user = Users.query.filter_by(username=auth_data.get('username')).first()
        
        if check_password_hash(user.password, auth_data.get('password')):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], 'HS256')
            return jsonify({'token': token}), 200
        abort(401, message="could not verify login")


# first route resource
class BookList(Resource):
    # @token_required
    def get(self, current_user):
        '''returns all books in the database'''
        books = BookModel.query.filter_by(user_id=current_user.id).all()
        allBooks = {}
        for book in books:
            allBooks[book.id] = {"title": book.title, "author": book.author}
            abort(404, message="no books available!")
        return allBooks


# 2nd route resource
class BookId(Resource):
    # @token_required
    @marshal_with(resource_fields)
    def get(self, book_id):
        '''returns book by id '''
        book = BookModel.query.filter_by(id=book_id).first()
        if not book:
            abort(404, message="No book found with that id!")
        return book

    @token_required
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

    @token_required
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

    @token_required
    def delete(self, book_id):
        '''deletes book from db with the provided id'''
        book = BookModel.query.filter_by(id=book_id).first()
        db.session.delete(book)
        return "Book deleted", 204
