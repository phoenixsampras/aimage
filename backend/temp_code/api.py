from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def post(self):
        args = parser.parse_args()
        data = {'task': args['task']}
        return data, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')


if __name__ == '__main__':
    app.run(debug=True)