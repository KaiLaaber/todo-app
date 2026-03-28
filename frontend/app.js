const API_URL = "http://127.0.0.1:5000/tasks";

async function loadTasks() {
    const res = await fetch(API_URL);
    const tasks = await res.json();
    const taskList = document.getElementById("task-list");
    taskList.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");
        li.innerHTML = `
        <span style="text-decoration: ${task.completed ? 'line-through' : 'none'}">
            ${task.title}
        </span>
        <button onclick='deleteTask(${task.id})'>❌</button>
        <button onclick='toggleTask(${task.id})'>${task.completed ? '➖' : '✔'}</button>`;
  
        taskList.appendChild(li);   
    });
}

loadTasks();

async function addTask() {
    const input = document.getElementById("taskInput");
    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title: input.value })
    });
    input.value = "";
    loadTasks();
}

async function deleteTask(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });
    loadTasks();
}

async function toggleTask(id) {
    await fetch(`${API_URL}/${id}/toggle`, {
        method: "PUT"
    });
    loadTasks();
}