from fastapi import FastAPI, HTTPException

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    completed: bool


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


@app.post("/tasks")
def create_task(task: TaskCreate):
    new_id = max(tasks.keys()) + 1

    new_task = {"id": new_id, "title": task.title, "completed": False}

    tasks[new_id] = new_task

    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    removed_task = tasks.pop(task_id, None)

    if removed_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    existing_task = tasks.get(task_id, None)

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task["title"] = task.title
    existing_task["completed"] = task.completed

    return existing_task
