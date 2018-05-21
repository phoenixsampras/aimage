from vendor.core.app import app
from models.picture_variant import PictureVariants
from models.tag import Tag
from vendor.module.load_db import db
from flask import request, jsonify
from service.tag.find_or_create_tag import findOrCreateTag
@app.route('/variant/tag', methods=['POST'])
def editTag():
    variant_id = request.get_json()['variant_id']
    tags =  request.get_json()['tags']
    for tag in tags:
        findOrCreateTag(tag)
    variant = PictureVariants.query.filter_by(id = variant_id).first()
    variant.tags  = tags
    db.session.commit()
    return jsonify({"isSuccess":True, "message":tags})