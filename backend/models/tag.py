from vendor.module.load_db import db
class Tag(db.Model): #declare Picture Table
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    def __repr__(self):
        return '<Tag %r>' % self.id