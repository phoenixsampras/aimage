
from clarifai.rest import ClarifaiApp
clarifai_app = ClarifaiApp(api_key='c26b563b4f694b3d93a503bb959233b2')
clarifai_app.inputs.delete_all()