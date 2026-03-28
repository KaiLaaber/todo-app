import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

app = Flask(__name__)



tasks = []
task_id = 1


@app.route('/')
def home():
    return 'Todo API is running!'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    rows = c.fetchall()

    conn.close()
    tasks = []

    for row in rows:
        tasks.append({
            'id': row[0],
            'title': row[1],
            'completed': bool(row[2])
        })

    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():

    data = request.get_json()
    
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (title) VALUES (?)', (data['title'],))

    conn.commit()
    conn.close()

    return jsonify(data), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    CORS(app)
    init_db()
    app.run(debug=True)
