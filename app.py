from flask import Flask, request, jsonify, render_template
from flasgger import Swagger

app = Flask(__name__)

swagger = Swagger(app)

todos = [
    {"id": 1, "task": "Learn Flask", "done": False},
    {"id": 2, "task": "Build REST API", "done": False}
]

@app.route('/')
def home():
    return render_template('index.html')

# GET all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todo-app')
def todo_app():
    return render_template('todo_app.html')


# GET a specific todo by ID
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    return jsonify(todo) if todo else ("Not found", 404)

# POST - create a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    new_data = request.json
    new_todo = {
        "id": len(todos) + 1,
        "task": new_data.get("task"),
        "done": False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# PUT - update an existing todo
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return ("Not found", 404)
    data = request.json
    todo["task"] = data.get("task", todo["task"])
    todo["done"] = data.get("done", todo["done"])
    return jsonify(todo)

# DELETE - remove a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return ("", 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
