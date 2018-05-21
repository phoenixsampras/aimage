from service.image_processing import imgProcessing
from models.picture import Picture
from models.picture_variant import PictureVariants
from service.check_is_first import checkIsFirst
from service.get_score import getScore
from vendor.module.load_db import db
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