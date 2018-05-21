import os
import importlib
from vendor.core.app import app
for root, dirs, files in os.walk("router"):
    for file in files:
        if(file.endswith('.py')):
            modulePath = os.path.join(root, os.path.splitext(file)[0]).replace('\\', '.')
            app.logger.info('loading router: '+ modulePath)
            importlib.import_module(modulePath)