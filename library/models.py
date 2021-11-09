from flask.helpers import make_response
from sqlalchemy.orm import backref, relationship
from flask import request, jsonify
from library.main import app, db
from functools import wraps
import jwt
from flask_restful import abort


# users table
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    books = db.relationship('BookModel', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

# books table
class BookModel(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # users = relationship("User")

    def ___repr__(self):
        return '<Book {}>'.format(self.title)


# token decorator 
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # pass jwt-token in headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token: # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)

        return f(current_user, *args, **kwargs)
    return decorator