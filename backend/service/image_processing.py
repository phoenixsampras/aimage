import base64
import math
MAX_HEADER= 100;
MAX_FOOTER= 100;
MAX_MIDDLE= 50;
class ImageInfo:
    def __init__(self, header, middle, footer, lens):
        self.header = header
        self.footer = footer
        self.middle = middle
        self.lens = lens
def path2base64(path):
    with open(path, 'rb') as im:
        return  base64.b64encode(im.read()).decode('utf8')

def imgProcessing(path):
    img64 = path2base64(path)
    lens = len(img64);
    header = img64[0:MAX_FOOTER]
    footer = img64[lens-MAX_FOOTER: lens]
    middle = img64[math.floor(lens/2): math.floor(lens/2) + MAX_MIDDLE]
    return ImageInfo(header,middle,footer,lens)
