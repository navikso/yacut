import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY', default='SUP3R')


CHARACTERS = '123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
SPECIAL_CHARS = '$&!,|.><-; '
PERMANENT_PART = 'http://localhost/'
