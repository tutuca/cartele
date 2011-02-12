# -*- coding: utf-8 -*-
from functools import wraps
from flask import redirect, url_for, request, session, flash

def login_required(f):
    """Redirect to login page if user not logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            flash(u'Hace falta iniciar sesión', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
