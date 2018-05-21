from models.tag import Tag
from vendor.module.load_db import db
def getTagByName(name):
    tag = Tag.query.filter_by(name=name);
    db.session.commit()
    print(tag)
