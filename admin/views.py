# -*- coding: utf-8 -*-
from flask import request, url_for, redirect, render_template, flash, session, g
from flaskext.uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import generate_password_hash, check_password_hash
from models import User, Banner, Author

uploaded_files = UploadSet('files', IMAGES)
configure_uploads(app, uploaded_files)

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('name')
        user = User.query.filter_by(username=username).first()
        if user.check_password(password):
            flash(u'Bienvenido %s' %username)
            session['username'] = username
            return redirect(url_for('index'))
        else: 
            flash(u'Usuario o contraseña incorrecto')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

def syncdb(app):
    with app.test_request_context():
        # The context is needed so db can access the configuration of the app
        db.create_all()
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    return "Initialized new empty database in %s" % db_uri
    
if __name__ == '__main__':
    app.run(debug=True)
