from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
import json, uuid

app = Flask(__name__)

DATA_FILE = Path("tasks.json")
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]")

def load_tasks():
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    tmp = DATA_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(tasks, indent=2))
    tmp.replace(DATA_FILE)

# Home / Dashboard
@app.route("/", methods=["GET", "POST"])
def dashboard():
    tasks = load_tasks()

    if request.method == "POST":
        # Add new task
        title = request.form.get("title")
        if title:
            new_task = {
                "id": str(uuid.uuid4()),
                "title": title,
                "done": False
            }
            tasks.append(new_task)
            save_tasks(tasks)
        return redirect(url_for("dashboard"))

    return render_template("dashboard.html", tasks=tasks)

# Mark task as done / toggle
@app.route("/toggle/<task_id>")
def toggle_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            break
    save_tasks(tasks)
    return redirect(url_for("dashboard"))

# Delete task
@app.route("/delete/<task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
