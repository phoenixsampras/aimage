from vendor.core.app import app
from models.picture_variant import PictureVariants
from models.tag import Tag
from vendor.module.load_db import db
from flask import request, jsonify
@app.route('/variant/tag', methods=['POST'])
def editTag():
    print(request.get_json())
    variant_id = request.get_json()['variant_id']
    tags =  request.get_json()['tags']
    variant = PictureVariants.query.filter_by(id = variant_id)
    variant.tags  = tags
    db.session.commit()
    return jsonify({"isSuccess":True, "message":tags})