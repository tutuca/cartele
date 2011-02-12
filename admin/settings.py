# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(__file__)

DEBUG = False

ADMINS = (
    ('etnalubma', 'francisco.herrero@gmail.com'),
    ('tutuca', 'maturburu@gmail.com'),
    ('ewock', 'onetti.martin@gmail.com'),
    ('sancho', 'santiago.videla@gmail.com'),
)

DEBUG_TB_INTERCEPT_REDIRECTS = True

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

SECRET_KEY = '7$57#ttr-tzqr*dt$l7vac0xt&1+i=gi^-y8bnsba$i%ci^nrd'

UPLOAD_FOLDER = '%s/banners' %BASE_DIR

from local_settings import *
