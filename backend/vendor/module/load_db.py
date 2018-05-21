from flask_sqlalchemy import SQLAlchemy
from vendor.core.app import app
POSTGRES = {
    'user': 'postgres',
    'pw': '123456',
    'db': 'clarifai',
    'host': 'localhost',
    'port': '5432',
}

def initDB():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db = SQLAlchemy(app)
    return db
db = initDB()