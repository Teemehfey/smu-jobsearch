import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):


    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    POSTS_PER_PAGE = 4

    POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'my_database',
    'host': 'localhost',
    'port': '5432'
}

    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False
