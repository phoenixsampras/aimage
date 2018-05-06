from flask_sqlalchemy import SQLAlchemy
POSTGRES = {
    'user': 'deverpham',
    'pw': 'xxxxxxxxx',
    'db': 'clarifai',
    'host': '192.168.1.101',
    'port': '5432',
}
   
def initDB(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db = SQLAlchemy(app) 
    return db
