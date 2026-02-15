from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QApplication, QHBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer, QTime
import sys

class MainApp(QMainWindow):
    def __init__(self):
        # Configs
        super().__init__()
        self.setWindowTitle("Digital Clock")
        self.setFixedSize(700, 300)
        self.move(650, 300)

        # Widgets
        self.clock_label = QLabel(self, text="")
        self.timer = QTimer(self)
        self.update_time()
        self.initUI()

    def initUI(self) -> None:
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.main_layout.addWidget(self.clock_label, alignment=Qt.AlignCenter)
        self.clock_label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(self.central_widget)

        
        font_id = QFontDatabase.addApplicationFont("/home/joao-miguel/Desktop/Projects/3_Digital_Clock/DS-DIGI.TTF")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.clock_label.setFont(QFont(font_family, 110))

        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        #CSS
        self.setStyleSheet("""
        QWidget{
            background-color: #1F0F1E;                   
        }

        QLabel{
            background-color: #2E172D;
            color: #27F228;
            padding: 13px;
            border-radius: 20px;                  
        }
        """)

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.clock_label.setText(current_time)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
