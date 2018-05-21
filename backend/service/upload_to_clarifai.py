from clarifai.rest import Image as ClImage
from middleware.clarifai import clarifai_app
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