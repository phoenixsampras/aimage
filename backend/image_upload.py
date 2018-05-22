# upload.py
import os 
from os.path import basename
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
app = ClarifaiApp(api_key='f0f793c5445349d2af95cf08cfb6c544')
FILE_NAME = 'image_list_7000.txt'
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
            custom_metadata = { "id": os.path.splitext(images[current_index])[0], "filename": images[current_index]}
            imageList.append(ClImage(file_obj=open("marcas\/"+images[current_index], 'rb'),metadata=custom_metadata))
        except IndexError:
            break
    app.inputs.bulk_create_images(imageList)
    counter = counter + batch_size
    current_batch = current_batch + 1
print (imageList)