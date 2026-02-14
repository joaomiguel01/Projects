from ..Repositories.TaskRepository import TaskRepository
from ..Models.Task import Task
from uuid import UUID

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self._task_repo = task_repo
    

    def add_task(self, title: str) -> Task:
        return self._task_repo.create(title)
    
    def get_all_tasks(self) -> list[Task]:
        return self._task_repo.read_all()
    
    def update_task(self, task: Task) -> bool:
        return self._task_repo.update(task)
    
    def delete_task(self, task_id: str) -> bool:
        return self._task_repo.delete(task_id)