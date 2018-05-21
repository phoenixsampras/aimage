from vendor.module.load_db import db
class Picture(db.Model): #declare Picture Table
    id= db.Column(db.Integer, primary_key=True)
    lens = db.Column(db.BigInteger, nullable = False)
    header = db.Column(db.Text, nullable = False)
    footer = db.Column(db.Text, nullable = False)
    middle = db.Column(db.Text, nullable = False)
    def __repr__(self):
        return '<Picture %r>' % self.id