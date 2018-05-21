from vendor.core.app import app
from flask import url_for
@app.route('/', methods=['GET'])
def hello_world():
    	#print('--------------------- GET request ------------------', file=sys.stderr)
	return """
			<html>
				<head>
					<title>Comparador de Imagenes</title>
                    <link rel="stylesheet" href="{}">
				</head>
				<body>
					<form method="POST" action="/task/compare" enctype=multipart/form-data>
						Subir archivo para comparar: <input type="file" name="image"><br /><br />
						<input type="submit" value="Comparar"><br />
					</form>
                    <hr>
                    <form method="POST" action="/task/upload" enctype=multipart/form-data>
						Subir archivo para agregar a clarifai: <input type="file" name="image"><br /><br />
						<input type="submit" value="subir"><br />
					</form>
				</body>
			</html>
			""".format(url_for('static', filename='style.css'))