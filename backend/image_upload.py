# upload.py
import os
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
app = ClarifaiApp(api_key='c26b563b4f694b3d93a503bb959233b2')
FILE_NAME = 'image_list.txt'
FILE_PATH = os.path.join(os.path.curdir, FILE_NAME)
# Counter variables
current_batch = 0
counter = 0
batch_size = 32
# print(open(FILE_PATH, encoding='utf-8').read())
with open(FILE_PATH) as data_file:
    images = [url.strip() for url in data_file]
    row_count = len(images)
    print("Total number of images:", row_count, images)
while(counter < row_count):
    print("Processing batch: #", (current_batch+1))
    imageList = []
    for current_index in range(counter, counter+batch_size - 1):
        try:
            imageList.append(ClImage(file_obj=open("marcas\/"+images[current_index], 'rb')))
        except IndexError:
            break
    app.inputs.bulk_create_images(imageList)
    counter = counter + batch_size
    current_batch = current_batch + 1