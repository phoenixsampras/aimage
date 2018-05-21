from vendor.core.app import app
from models.picture_variant import PictureVariants
from vendor.module.load_db import db
from flask import request, jsonify
@app.route('/variant/order', methods=['POST'])
def orderChange():
    oldorder = request.get_json()['oldorder']
    inputid= request.get_json()['input_id']
    newOrder = request.get_json()['new_order']
    pictureVList = PictureVariants.query.filter_by(input_id = inputid, order = oldorder)
    for picture in pictureVList:
        picture.order = newOrder
        db.session.commit()
    return jsonify({"isSuccess":True, "message":"Changed Order"})