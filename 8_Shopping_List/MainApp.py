from PyQt5.QtWidgets import QApplication
from .Views.ShopView import MainWindow
from .Services.ShopService import ShopService
from .Repositories.ShopRepository import ShopRepository
import sys

class MainApp:
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._repo = ShopRepository()
        self._t_service = ShopService(self._repo)
        self._window = MainWindow(self._t_service)
    
    def run(self) -> None:
        self._window.show()
        sys.exit(self._app.exec())



if __name__ == "__main__":
    app_window = MainApp()
    app_window.run()