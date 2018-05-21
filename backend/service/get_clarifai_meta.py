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