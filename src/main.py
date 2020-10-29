"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/todo/<username>', methods=['GET'])
def get_todos(username):
    todos = Todo.query.filter_by(user_name = username)
    todos = list(map(lambda x: x.serialize(), todos))
    return jsonify(todos), 200

@app.route('/todo/<username>', methods=['POST'])
def post_todo(username):
    body = request.get_json()
    exists = Todo.query.filter_by(user_name = username, label = body['label']).first()
    if exists is not None:
        raise APIException('you already have this todo', status_code = 404)
    todo = Todo(label = body['label'], done = body['done'], user_name = username)
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.serialize()), 200

@app.route('/todo/<int:id>', methods=['PUT'])
def put_todo(id):
    body = request.get_json()
    todo_item = Todo.query.get(id)    
    print("MYTODOITEM", todo_item)
    todo_item.done = body['done']
    todo_item.label = body['label']
    db.session.commit()
    updated_item = Todo.query.get(id)
    updated_item = updated_item.serialize()
    return jsonify(updated_item), 200

@app.route('/todo/<username>/<int:id>', methods=['DELETE'])
def delete_todo(username, id):
    todo = Todo.query.get(id)
    if todo is None:
        raise APIException('entry does not exist', status_code = 400)
    db.session.delete(todo)
    db.session.commit()
    todos = Todo.query.filter_by(user_name = username)
    todos = list(map(lambda x: x.serialize(), todos))
    return jsonify(todos), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
