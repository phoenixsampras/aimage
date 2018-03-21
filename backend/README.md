## Setup
```
pip install -r requirements.txt
```

## Remove All images from clarifai
```
python ./remove_all.py
```
## upload image from 'image_list.txt'
```
python ./image_upload.py
```
## Start Server for Demo
### Run For Debug
```
python ./server.py
```

### Run For Server
```
sudo npm install -g forever
forever start -c python ./server.py
forever stop ./server.py
```


### Unusable Code
./temp_code