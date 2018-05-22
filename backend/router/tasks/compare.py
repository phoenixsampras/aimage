from vendor.core.app import app
from flask import request, jsonify
from vendor.helper.create_new_folder import create_new_folder
from werkzeug import secure_filename
from middleware.clarifai import clarifai_app
from service.get_clarifai_meta import getclarifaimeta
from service.add_record_to_database import addRecordToDatabase
from service.get_result import getResult
import os
@app.route('/task/compare', methods=['POST'])
def compare():
    print(request.files['image'])
    if request.files['image']:
        print('yes')
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['image']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)
        try:
            search = clarifai_app.inputs.search_by_image(fileobj=open(saved_path, 'rb'),per_page=200)
            #return the results in Rest/json format
            arr_search = []
            links=[]
            for search_result in search:
                imageObject = getclarifaimeta(search_result)
                arr_search.append(imageObject)
            imgid = addRecordToDatabase(saved_path, arr_search)
            results = getResult(imgid);
            return jsonify(results)

        except IndexError as e:
            print("error ")
            return jsonify({"isSuccess":False, "error":e})
    else:
        print('no')
        return jsonify('Where is image?')