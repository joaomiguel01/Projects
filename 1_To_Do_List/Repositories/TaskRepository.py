from ..Models.Task import Task
import os
import json

class TaskRepository:
    def __init__(self, db_name: str="task.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._db_name = os.path.join(base_dir, db_name)

        if not os.path.exists(self._db_name):
            with open(self._db_name, "x", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)
    
    
    def grab_data(self) -> list[dict]:
        with open(self._db_name, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def save_data(self, data: list[dict]) -> None:
        with open(self._db_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    

    def create(self, title: str) -> Task:
        tasks = self.grab_data()

        task = Task(title=title)
        
        tasks.append(task.to_dict())
        self.save_data(tasks)

        return task
    
    def read_all(self) -> list[Task]:
        tasks = self.grab_data()

        return [Task.from_dict(t) for t in tasks]
    
    def read_by_id(self, task_id: str) -> Task | None:
        tasks = self.grab_data()

        for t in tasks:
            if t["task_id"] == task_id:
                return Task.from_dict(t)
            
        return None
    
    def update(self, task: Task) -> bool:
        tasks = self.grab_data()

        for i, t in enumerate(tasks):
            if t["task_id"] == str(task.task_id):
                tasks[i] = task.to_dict()
                self.save_data(tasks)
                return True
        
        return False
    
    def delete(self, task_id: str) -> bool:
        tasks = self.grab_data()

        new_tasks = [t for t in tasks if t["task_id"] != task_id]

        if len(tasks) == len(new_tasks):
            return False
        
        self.save_data(new_tasks)
        return True
        
        
        