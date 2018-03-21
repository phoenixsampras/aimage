# search.py
from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key='c26b563b4f694b3d93a503bb959233b2')
# Search using a URL
search = app.inputs.search_by_image(url='http://sports-dev.calm-health.com:5000/image?filename=1.png')
for search_result in search:
    print("Score:", search_result.score, "| URL:", search_result.url)