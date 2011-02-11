import settings
from flask import Flask, request, url_for, redirect, render_template, flash, session, g
from flaskext.sqlalchemy import SQLAlchemy, BaseQuery
from flaskext.uploads import UploadSet, configure_uploads, IMAGES
from flaskext.debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

uploaded_files = UploadSet('files', IMAGES)
configure_uploads(app, uploaded_files)


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
    '''
    Used for profile and simple auth.
    '''
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

@app.route('/')
def index():
    authors = Author.query.all()
    return render_template('index.html', authors=authors)

@app.route('/author', methods=['GET', 'POST'])
def author():    
    if request.method == 'POST':
        author = Author(request.form.get(u'name'), request.form.get(u'email'))
        db.session.add(author)
        db.session.commit()
        flash("Author saved.")
        return redirect(url_for('index'))
    return render_template('author.html')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    authors = Author.query.all()
    if request.method == 'POST' and 'image' in request.files:
        image = request.form.files('image')
        data = request.form
        filename = uploaded_files.save(image)
        rec = Banner(
                filename=filename, 
                created_by=g.user.id,
                author_id=data.get('author'),
                destination=data.get('destination'),
                )
        rec.store()
        flash("Banner saved.")
        return redirect(url_for('index'))
    return render_template('upload.html', authors=authors)


def syncdb(app):
    with app.test_request_context():
        # The context is needed so db can access the configuration of the app
        db.create_all()
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    return "Initialized new empty database in %s" % db_uri
    
if __name__ == '__main__':
    app.run(debug=True)
