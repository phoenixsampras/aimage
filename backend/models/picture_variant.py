from vendor.module.load_db import db
from sqlalchemy.inspection import inspect
class PictureVariants(db.Model): #declare PictureVariants Table
    id= db.Column(db.Integer, primary_key=True)
    input_id =db.Column(db.String, unique=False)
    url = db.Column(db.String,  nullable= False)
    metafilename = db.Column(db.String, nullable= False)
    metaid = db.Column(db.String, nullable= False)
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'), nullable= False)
    score = db.Column(db.Float, nullable = False)
    is_remove = db.Column(db.Boolean, default = False)
    original_order = db.Column(db.Integer, nullable = False)
    order = db.Column(db.Integer, nullable = False)
    tag = db.Column(db.Integer(), db.ForeignKey('tag.id'), nullable = False)
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
    def serialize_list(l):
        return [m.serialize() for m in l]
    def __repr__(self):
        return '<PictureVariants %r>' % self.id