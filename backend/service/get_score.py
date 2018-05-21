from models.picture_variant import PictureVariants
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