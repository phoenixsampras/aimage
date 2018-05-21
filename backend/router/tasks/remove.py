from vendor.core.app import app
from flask import request, jsonify
from vendor.module.load_db import db
from models.picture_variant import PictureVariants
@app.route('/task/remove', methods=['POST'])
def remove():
    if request.method == 'POST':
        input_id = request.get_json()['input_id'];
        order = request.get_json()['order'];
        pictureVList = PictureVariants.query.filter_by(input_id = input_id, order = order)
        for pictureV in pictureVList:
            pictureV.is_remove = True
            db.session.commit()
        return jsonify({"isSuccess":True, "message":"Removed from list result"})