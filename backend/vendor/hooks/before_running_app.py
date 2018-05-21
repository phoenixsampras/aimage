from flask_cors import CORS
from vendor.core.app import app
import os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.logger.info('set config before run app')
import vendor.module.load_router
import vendor.module.load_db
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
cors = CORS(app, resources={r"*": {"origins": "*"}})
