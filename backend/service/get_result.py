
from models.picture_variant import PictureVariants
def getResult(imgid):
    results = PictureVariants.query.filter_by(picture_id=imgid, is_remove=False).all()
    return PictureVariants.serialize_list(results)