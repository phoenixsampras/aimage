from flask_sqlalchemy import SQLAlchemy
from vendor.core.app import app
POSTGRES = {
    'user': 'odoo',
    'pw': '123456',
    'db': 'FEGASACRUZ',
    'host': '9.9.9.20',
    'port': '5432',
}

def initDB():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db = SQLAlchemy(app)
    return db
db = initDB()