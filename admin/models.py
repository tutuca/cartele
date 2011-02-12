from flaskext.sqlalchemy import SQLAlchemy, BaseQuery
from werkzeug import generate_password_hash, check_password_hash
from admin import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String(), unique=True)
    def __init__(self, name, email):
        self.name = name
        self.email = email
 

    def __repr__(self):
        return self.name


class Click(object):
    __tablename__ = 'clicks'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    origin = db.Column(db.String)
    banner_id = db.Column(db.Integer)
    
class Banner(object):
    '''
    Banner, stores a image, destination, and click count
    '''
    __tablename__ = 'banners'
    id = db.Column(db.Integer, primary_key=True)
    clicks = db.Column(db.Integer)
    filename = db.Column(db.String, unique=True)
    destination = db.Column(db.String)
    author_id = db.Column(db.Integer)
    created_by = db.Column(db.Integer)

    def __init__(self, filename, destination, author_id, created_by):
        self.filename = filename
        self.destination = destination
        self.author_id = author_id
        self.created_by = created_by

