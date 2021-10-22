from library import db
from flask import request, jsonify
from library import app
from functools import wraps
import jwt


# user model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(60))
    password = db.Column(db.String(32))
    admin = db.Column(db.Boolean)

    def ___repr__(self):
        return f'<User: {self.username}>'


# books table
class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))


# token generator 
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing!'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Invalid token!'})

        return f(current_user, *args, **kwargs)
    return decorator