from uuid import UUID, uuid4

class Task:
    def __init__(self, title: str, task_id: UUID | None=None):
        self._task_id = task_id or uuid4()
        self.title = title


    @property
    def task_id(self) -> UUID:
        return self._task_id
    
    @property
    def title(self) -> str:
        return self._title
    @title.setter
    def title(self, t: str) -> None:
        if not (isinstance(t, str) and t.strip()):
            raise ValueError("The title can't be a blank string!")
        
        if len(t) < 8:
            raise ValueError("The tasks must be at least 8 characteres long!")
        
        self._title = t.strip().upper()
    

    @classmethod
    def from_dict(cls, t: dict) -> "Task":
        return cls(
            task_id=UUID(t['task_id']),
            title=t['title']
        )
    
    def to_dict(self) -> dict:
        return {
            'task_id': str(self.task_id),
            'title': self.title
        }
    