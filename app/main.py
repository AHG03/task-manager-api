from fastapi import FastAPI, HTTPException

app = FastAPI()
tasks = {
    1: {"id": 1, "title": "Grocery", "completed": False},
    2: {"id": 2, "title": "Laundry", "completed": False},
    3: {"id": 3, "title": "Clean Room", "completed": False}
}


@app.get("/tasks")
def get_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
