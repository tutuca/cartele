# -*- coding: utf-8 -*-
import os
from flask import request, url_for, redirect, render_template, flash, session, g
from models import db, User, Banner, Author
from admin import app
from forms import AuthorForm, BannerForm, LoginForm
from decorators import login_required

@app.route('/')
def index():
    authors = Author.query.all()
    return render_template('index.html', authors=authors)

@app.route('/author', methods=['GET', 'POST'])
@login_required
def author():    
    form = AuthorForm(request.form)
    if request.method == 'POST' :
        author = Author(request.form.get(u'name'), request.form.get(u'email'))
        db.session.add(author)
        db.session.commit()
        flash("Autor guardado.")
        return redirect(url_for('index'))
    return render_template('author.html', form=form)
    
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    authors = Author.query.all()
    form = BannerForm(request.form)
    form.author_id.choices = [(a.id, a.name) for a in authors]
    if request.method == 'POST' and 'image' in request.files:
        image_data = request.FILES[form.image.name].read()
        open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)

        rec = Banner(
                filename=filename, 
                created_by=g.user.id,
                author_id=data.get('author'),
                destination=data.get('destination'),
                )
        rec.store()
        flash("Banner guardado.")
        return redirect(url_for('index'))
    return render_template('upload.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.data.get('name')
        password = form.data.get('password')
        user = User.query.filter_by(username=username).first_or_404()
        if user.check_password(password):
            flash(u'Bienvenido %s' %username)
            session['username'] = username
            return redirect(url_for('index'))
        else: 
            flash(u'Usuario o contraseña incorrecto')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
