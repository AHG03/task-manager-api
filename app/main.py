from fastapi import FastAPI

app = FastAPI()
tasks = {
    1: {"id": 1, "title": "Grocery", "completed": False},
    2: {"id": 2, "title": "Laundry", "completed": False},
    3: {"id": 3, "title": "Clean Room", "completed": False}
}


@app.get("/tasks")
def get_tasks():
    return list(tasks.values())
