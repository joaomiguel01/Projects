from PyQt5.QtWidgets import QApplication
from .Views.TaskView import MainScreen
from .Services.TaskService import TaskService
from .Repositories.TaskRepository import TaskRepository
import sys

class MainApp:
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._repo = TaskRepository()
        self._t_service = TaskService(self._repo)
        self._window = MainScreen(self._t_service)
    
    def run(self) -> None:
        self._window.show()
        sys.exit(self._app.exec())



if __name__ == "__main__":
    app_window = MainApp()
    app_window.run()