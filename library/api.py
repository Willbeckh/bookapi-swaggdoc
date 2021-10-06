from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# class BookModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200))
#     author = db.Column(db.String(200))


# db.create_all() # command to create db

# database object
books = {
    1: {'title': 'code book', 'author': 'Billy_dev'},
    2: {'title': 'no fuckery', 'author': 'Manson'}
}


book_post_args = reqparse.RequestParser()
book_post_args.add_argument("title", type=str, help="Title is required!", required=True)
book_post_args.add_argument("author", type=str, help="author is required!", required=True)

book_update_args = reqparse.RequestParser()
book_update_args.add_argument("title", required=True)
book_update_args.add_argument("author", required=True)

class BookList(Resource):
    def get(self):
        '''returns all books in the database'''
        return books

class BookId(Resource):
    def get(self, book_id):
        '''returns book by id '''
        return books[book_id]  

    def post(self, book_id):
        args = book_post_args.parse_args()
        if book_id in books:
            abort(409)

        books[book_id] = {
            "title": args["title"],
            "author": args["author"]
        }
        return books[book_id]

    def put(self, book_id):
        '''updates a book using its id'''
        args = book_update_args.parse_args()
        if book_id not in books:
            abort(404)
        if args['title']:
            books[book_id]["title"] = args["title"]
        if args["author"]:
            books[book_id]["author"] = args["author"]
        return books[book_id]

    def delete(self, book_id):
        del books[book_id]
        return books

api.add_resource(BookList, "/bookapi/books") # gets all the books in the db.
api.add_resource(BookId, "/bookapi/books/<int:book_id>") # use this to get/post a book

    
if __name__ == '__main__':
    app.run(debug=True)