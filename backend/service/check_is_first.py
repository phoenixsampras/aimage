def checkIsFirst(array_search):
    isFirst = True;
    imageData = {};
    for search_result in array_search:
        if search_result['score'] > 0.8:
            isFirst = False
            imageData = search_result
            break
    return isFirst,imageData;