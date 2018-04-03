from flask import Flask, json, jsonify, url_for, send_from_directory, request, render_template, send_file
import logging
import os
from werkzeug import secure_filename
import sys
from flask_cors import CORS
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
clarifai_app = ClarifaiApp(api_key='c26b563b4f694b3d93a503bb959233b2')
# HOST_URL_PORT='http://sports-dev.calm-health.com:5000/'
# HOST_URL_PORT='http://9.9.9.113:5000/'
HOST_URL_PORT='http://localhost:5000/'
app = Flask(__name__)
file_handler = logging.FileHandler('zServer.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

def upload_to_clarifai(search, saved_path):
    isFirst = True
    for search_result in search:
        if search_result.score > 0.99:
            isFirst = False
            break
    if isFirst:
        imageList = []
        imageList.append(ClImage(file_obj=open(saved_path, 'rb')))
        clarifai_app.inputs.bulk_create_images(imageList)
    return isFirst

@app.route('/task/<task>', methods=['GET', 'POST'])
def task(task):
    app.logger.info(PROJECT_HOME)

    if task == 'compare':
        if request.method == 'POST' and request.files['image']:
            app.logger.info(app.config['UPLOAD_FOLDER'])
            img = request.files['image']
            print(img)
            print(type(img))
            img_name = secure_filename(img.filename)
            create_new_folder(app.config['UPLOAD_FOLDER'])
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            app.logger.info("saving {}".format(saved_path))
            img.save(saved_path)

            try:
                search = clarifai_app.inputs.search_by_image(fileobj=open(saved_path, 'rb'))
                #return the results in Rest/json format
                arr_search = []
                for search_result in search:
                    arr_search.append({"score":search_result.score, "url": search_result.url})

                return jsonify(arr_search)

            except IndexError as e:
                print("error ")
                return jsonify({"isSuccess":False, "error":e})
        else:
            return jsonify('Where is image?')
    if task == 'upload':
        if request.method == 'POST' and request.files['image']:
            app.logger.info(app.config['UPLOAD_FOLDER'])
            img = request.files['image']
            img_name = secure_filename(img.filename)
            create_new_folder(app.config['UPLOAD_FOLDER'])
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            app.logger.info("saving {}".format(saved_path))
            img.save(saved_path)

            try:
                search = clarifai_app.inputs.search_by_image(fileobj=open(saved_path, 'rb'))
                #return the results in Rest/json format
                isFirst = upload_to_clarifai(search, saved_path)
                arr_search = []
                for search_result in search:
                    arr_search.append({"score":search_result.score, "url": search_result.url})
                if isFirst:
                    return jsonify({"isSuccess":isFirst, "message":"Successfully uploaded to clarifai.","searchResult":arr_search})
                else:
                    return jsonify({"isSuccess":isFirst, "message":"Already exist on the clarifai.","searchResult":arr_search})

            except IndexError as e:
                print("error ")
                return jsonify({"isSuccess":False, "message":"Some Exception occur", "error":e })
        else:
            return jsonify('Where is image?')

@app.route('/image', methods=['GET'])
def api_image():
    filename = request.args.get('filename', default = '*', type = str)
    if(os.path.isfile('./uploads/{}'.format(filename))):
        return send_file('./uploads/{}'.format(filename), mimetype='image/gif')
    else:
        return 'Cannot find file {}'.format(filename)

@app.route('/', methods=['GET'])
def hello_world():
	#print('--------------------- GET request ------------------', file=sys.stderr)
	return """
			<html>
				<head>
					<title>Comparador de Imagenes</title>
                    <link rel="stylesheet" href="{}">
				</head>
				<body>
					<form method="POST" action="/task/compare" enctype=multipart/form-data>
						Subir archivo para comparar: <input type="file" name="image"><br /><br />
						<input type="submit" value="Comparar"><br />
					</form>
                    <hr>
                    <form method="POST" action="/task/upload" enctype=multipart/form-data>
						Subir archivo para agregar a clarifai: <input type="file" name="image"><br /><br />
						<input type="submit" value="subir"><br />
					</form>
				</body>
			</html>
			""".format(url_for('static', filename='style.css'))

if __name__ == '__main__':
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True)
