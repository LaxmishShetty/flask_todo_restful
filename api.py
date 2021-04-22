from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

parser = reqparse.RequestParser()
parser.add_argument('task')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


def abort_if_todo_doesnot_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message='Todo {} does not exist'.format(todo_id))


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnot_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnot_exist(todo_id)
        del TODOS[todo_id]
        return '', 200

    def put(self, todo_id):
        abort_if_todo_doesnot_exist(todo_id)
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


class Todolist(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo' + str(todo_id)
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 200


api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Todolist, '/todos')

if __name__ == '__main__':

    app.run(debug=True)

