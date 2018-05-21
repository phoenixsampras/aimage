from vendor.core.app import app
from models.picture_variant import PictureVariants
from vendor.module.load_db import db
from flask import request, jsonify
@app.route('/variant/reset', methods=['POST'])
def variantReset():
    picture_id = request.get_json()['picture_id']
    pictureVList = PictureVariants.query.filter_by(picture_id = picture_id)
    for picture in pictureVList:
        picture.is_remove= False
        picture.order = picture.original_order
        db.session.commit()
    return jsonify({"isSuccess":True, "message":"reset successfully"})