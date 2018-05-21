from vendor.core.app import app
from flask import request, jsonify
from vendor.helper.create_new_folder import create_new_folder
from werkzeug import secure_filename
from middleware.clarifai import clarifai_app
from service.getclarifaimeta import getclarifaimeta
from service.add_record_to_database import addRecordToDatabase
from service.get_result import getResult
from service.upload_to_clarifai import upload_to_clarifai
import os
@app.route('/task/upload', methods=['POST'])
def upload():
    if request.files['image']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['image']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)

        try:
            search = clarifai_app.inputs.search_by_image(fileobj=open(saved_path, 'rb'))
            arr_search = []
            #return the results in Rest/json format
            isFirst = upload_to_clarifai(search, saved_path)
            for search_result in search:
                imageObject = getclarifaimeta(search_result)
                arr_search.append(imageObject)
            imgid = addRecordToDatabase(saved_path, arr_search)
            results = getResult(imgid);
            if isFirst:
                return jsonify({"isSuccess":isFirst, "message":"Successfully uploaded to clarifai.","searchResult":results})
            else:
                return jsonify({"isSuccess":isFirst, "message":"Already exist on the clarifai.","searchResult":results})

        except IndexError as e:
            print("error ")
            return jsonify({"isSuccess":False, "message":"Some Exception occur", "error":e })
    else:
        return jsonify('Where is image?')