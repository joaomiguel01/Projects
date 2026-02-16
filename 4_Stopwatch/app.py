from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
                             QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer
import sys

class MainApp(QWidget):
    def __init__(self):
        # Configs
        super().__init__()
        self.setWindowTitle("Stopwatch")
        self.setFixedSize(800, 400)
        self.move(650, 300)
        self.miliseconds = 0

        # Widgets
        self.display_label = QLabel(self, text="00:00:00:000")
        self.start_button = QPushButton(self, text="Start")
        self.start_button.clicked.connect(self.start_timer)
        self.stop_button = QPushButton(self, text="Stop")
        self.stop_button.clicked.connect(self.stop_timer)
        self.reset_button = QPushButton(self, text="Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.initUI()

    
    def initUI(self) -> None:
        self.hbox_buttons = QHBoxLayout()
        self.main_layout = QVBoxLayout()

        self.hbox_buttons.addWidget(self.start_button)
        self.hbox_buttons.addWidget(self.stop_button)
        self.hbox_buttons.addWidget(self.reset_button)

        self.main_layout.addWidget(self.display_label, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.hbox_buttons)
        self.setLayout(self.main_layout)

        # UI Configs
        self.display_label.setFixedWidth(750)
        self.display_label.setFixedHeight(200)
        self.display_label.setAlignment(Qt.AlignCenter)

        self.start_button.setCursor(Qt.PointingHandCursor)
        self.stop_button.setCursor(Qt.PointingHandCursor)
        self.reset_button.setCursor(Qt.PointingHandCursor)

        # CSS
        self.setStyleSheet("""
        QLabel{
            background-color: #BFFDFF;
            font-size: 100px;
            padding: 5px;
            font-family: monospace;
            border-radius: 15px;                   
        }
                           
        QPushButton{
            font-size: 45px;               
        }
        """)
    
    def start_timer(self) -> None:
        if not self.timer.isActive():
            self.timer.start(10)

    def stop_timer(self) -> None:
        if self.timer.isActive():
            self.timer.stop()

    def reset_timer(self) -> None:
        self.timer.stop()
        self.miliseconds = 0
        self.display_label.setText("00:00:00:000")
    
    def update_timer(self) -> None:
        self.miliseconds += 10

        hours = self.miliseconds // 3600000
        mins = (self.miliseconds % 3600000) // 60000
        secs = (self.miliseconds % 60000) // 1000
        ms = self.miliseconds % 1000

        self.display_label.setText(f"{hours:02}:{mins:02}:{secs:02}:{ms:03}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())