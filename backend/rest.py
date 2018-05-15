from flask import Flask, json, jsonify, url_for, send_from_directory, request, render_template, send_file
import logging
import os
from werkzeug import secure_filename
import sys
from sqlalchemy.inspection import inspect
from flask_cors import CORS
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import base64
from models.db import initDB
from service.imgProcessing import imgProcessing
clarifai_app = ClarifaiApp(api_key='c650f1c0094a4dd2b6021ca7175c88e5')
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
db= initDB(app)

class Picture(db.Model): #declare Picture Table
    id= db.Column(db.Integer, primary_key=True)
    lens = db.Column(db.BigInteger, nullable = False)
    header = db.Column(db.Text, nullable = False)
    footer = db.Column(db.Text, nullable = False)
    middle = db.Column(db.Text, nullable = False)
    def __repr__(self):
        return '<Picture %r>' % self.id

class PictureVariants(db.Model): #declare PictureVariants Table
    id= db.Column(db.Integer, primary_key=True)
    input_id =db.Column(db.String, unique=False)
    url = db.Column(db.String,  nullable= False)
    metafilename = db.Column(db.String, nullable= False)
    metaid = db.Column(db.String, nullable= False)
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'), nullable= False)
    score = db.Column(db.Float, nullable = False)
    is_remove = db.Column(db.Boolean, default = False)
    original_order = db.Column(db.Integer, nullable = False)
    order = db.Column(db.Integer, nullable = False)
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
    def serialize_list(l):
        return [m.serialize() for m in l]
    def __repr__(self):
        return '<PictureVariants %r>' % self.id
def getScore(image, list_result):
    ids = []
    for result in list_result:
        ids.append(result['input_id'])
    images = PictureVariants.query.filter_by(picture_id = image.id)
    score = 0
    for image in images:
        if(image.input_id in ids):
            score+=1
    return score;
def addRecordToDatabase(path, arr_search):
    imgInfo = imgProcessing(path)
    image = Picture.query.filter_by(lens = imgInfo.lens, header = imgInfo.header, footer = imgInfo.footer, middle = imgInfo.middle).first()
    if(image is None):
        image = Picture(lens = imgInfo.lens, header = imgInfo.header, footer = imgInfo.footer, middle = imgInfo.middle)
        db.session.add(image)
        db.session.commit()
        db.session.refresh(image)
    isFirst, imageData = checkIsFirst(arr_search)
    if(not isFirst):
        print('not first')
        parentRoot = PictureVariants.query.filter(PictureVariants.input_id == imageData['input_id'], PictureVariants.order <=4,PictureVariants.is_remove == False);
        maxScore = -1;
        maxId = -1;
        for parent in parentRoot:
            score = getScore(parent, arr_search);
            if( score > maxScore):
                maxId = parent.picture_id
                maxScore = score
        list_search = PictureVariants.query.filter_by(picture_id = maxId, is_remove=False).order_by(PictureVariants.order).limit(5)
        arr_search = PictureVariants.serialize_list(list_search) + arr_search;
    for index,search in enumerate(arr_search):
        variant = PictureVariants.query.filter_by(url = search['url'], input_id = search['input_id'], picture_id= image.id).first()
        if(variant is None):
            variant = PictureVariants(picture_id=image.id, url= search['url'], score= search['score'], original_order=index, order = index, input_id= search['input_id'],metafilename = search['metafilename'], metaid = search['metaid'])
            db.session.add(variant)
            db.session.commit()

    return image.id;

def getResult(imgid):
    results = PictureVariants.query.filter_by(picture_id=imgid, is_remove=False).all()
    return PictureVariants.serialize_list(results)

def getclarifaimeta(image):
    imageObject = {"score":image.score, "url": image.url}
    imageObject['input_id'] = image.input_id
    if(image.metadata is None):
        imageObject['metafilename'] = '';
        imageObject['metaid'] = ''
    else:
        imageObject['metafilename'] = image.metadata['filename']
        imageObject['metaid'] = image.metadata['id']
    return imageObject
def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath
def checkIsFirst(array_search):
    isFirst = True;
    imageData = {};
    for search_result in array_search:
        if search_result['score'] > 0.9:
            isFirst = False
            imageData = search_result
            break
    return isFirst,imageData;
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
            img_name = secure_filename(img.filename)
            create_new_folder(app.config['UPLOAD_FOLDER'])
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            app.logger.info("saving {}".format(saved_path))
            img.save(saved_path)
            try:
                search = clarifai_app.inputs.search_by_image(fileobj=open(saved_path, 'rb'))
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
    if task == 'remove':
        if request.method == 'POST':
            input_id = request.get_json()['input_id'];
            order = request.get_json()['order'];
            pictureVList = PictureVariants.query.filter_by(input_id = input_id, order = order)
            for pictureV in pictureVList:
                pictureV.is_remove = True
                db.session.commit()
            return jsonify({"isSuccess":True, "message":"Removed from list result"})
            
@app.route('/image', methods=['GET'])
def api_image():
    filename = request.args.get('filename', default = '*', type = str)
    if(os.path.isfile('./uploads/{}'.format(filename))):
        return send_file('./uploads/{}'.format(filename), mimetype='image/gif')
    else:
        return 'Cannot find file {}'.format(filename)

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
    
@app.route('/variant/reset', methods=['POST'])
def variantReset():
    picture_id = request.get_json()['picture_id']
    pictureVList = PictureVariants.query.filter_by(picture_id = picture_id)
    for picture in pictureVList:
        picture.is_remove= False
        picture.order = picture.original_order
        db.session.commit()
    return jsonify({"isSuccess":True, "message":"reset successfully"})
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
    db.create_all()
    app.run(host='0.0.0.0', debug=True)
