from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt
from .db import quotes
from random import randint
import sys

class MainApp(QWidget):
    def __init__(self):
        # Configs
        super().__init__()
        self.setWindowTitle("Quote Generator")
        self.setFixedSize(700, 500)
        self.move(650, 300)

        # Widgets
        self.quote_label = QLabel(self, text="Click the button to generate a quote ✨")
        self.generate_button = QPushButton(self, text="Generate")

        self.initUI()
    
    def initUI(self) -> None:
        # Layouts
        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.quote_label, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)

        self.setLayout(self.main_layout)

        # UI Configs
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.quote_label.setAlignment(Qt.AlignCenter)
        self.quote_label.setWordWrap(True)
        self.generate_button.setCursor(Qt.PointingHandCursor)

        # CSS
        self.setStyleSheet("""
        QWidget {
            background-color: #1E151F;
            font-family: Segoe UI;
            font-size: 30px;                
        }
                           
        QLabel {
            background-color: #412D42;
            color: white;
            padding: 20px;
            border-radius: 20px;
            margin-top: 50px;
            font-weight: 600;                
        }
                           
        QPushButton {
            background-color: #6C63FF;
            padding: 15px;
            max-width: 200px;
            font-weight: bold;
            color: white;
            border-radius: 20px;                    
        }
                           
        QPushButton:hover {
            background-color: #857DFF;
        }
                           
        QPushButton:pressed {
            background-color: #4A42D4;
        }
        """)

        # Control Configs
        self.generate_button.clicked.connect(self.generate_quote)
    
    def generate_quote(self) -> None:
        quote_id = randint(0, (len(quotes)-1))
        self.quote_label.setText(quotes[quote_id])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())