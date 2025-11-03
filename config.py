import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://murat:murat@servinfo-maria/DBmurat')
BOOTSTRAP_SERVE_LOCAL = True

SECRET_KEY = "1w{euOn#)\x0c<EA0RO7O>8|w0"
