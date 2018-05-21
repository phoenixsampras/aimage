from models.tag import Tag
from vendor.module.load_db import db
def createTagByName(name):
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    db.session.refresh(tag)
    return tag.name
def findOrCreateTag(name):
    tag = Tag.query.filter_by(name=name).first()
    if(tag is None):
        name = createTagByName(name)
        return name
    else:
        return tag.id;
