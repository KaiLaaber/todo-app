from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

tasks = []
task_id = 1


@app.route('/')
def home():
    return 'Todo API is running!'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    global task_id
    data = request.get_json()
    task = {
        'id': task_id,
        'title': data,
        'completed': False
    }
    print(f"Created task: {task['id']} - {task['title']}")
    tasks.append(task)
    task_id += 1
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)
