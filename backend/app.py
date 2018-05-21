
from vendor.core.app import app
import vendor.hooks.before_running_app 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

