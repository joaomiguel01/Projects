from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
                             QApplication)
from PyQt5.QtCore import Qt
import sys
import string
from secrets import choice

class PassGenerator(QWidget):
    def __init__(self):
        # Configs
        super().__init__()
        self.setWindowTitle("Passowrd Generator")
        self.setFixedSize(600, 400)
        self.move(700, 300)

        # Widgets
        self.password_label = QLabel(self, text="")
        self.generate_button = QPushButton(self, text="Generate")

        self.initUI()
    
    
    def initUI(self) -> None:
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.main_layout.addWidget(self.password_label, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)

        self.setLayout(self.main_layout)

        # UI Configs
        self.password_label.setAlignment(Qt.AlignCenter)
        self.generate_button.setCursor(Qt.PointingHandCursor)
        self.generate_button.clicked.connect(self.generate_password)

        # CSS
        self.setStyleSheet("""
        QWidget{
            background-color: #202036;
            font-size: 16px;
        }
                           
        QLabel{
            background-color: #3C3C5C;
            width: 500px;
            padding: 20px;
            font-size: 40px;
            font-weight: bold;
            color: white;
            border-radius: 10px; 
            font-family: Consolas;            
        }
                           
        QPushButton{
            background-color: #FF9F1A;
            color: black;
            border-radius: 10px;
            font-size: 30px;
            font-weight: bold;
            max-width: 200px;
            padding: 30px;                   
        }
                           
        QPushButton:hover{
            background-color: #FFC273;                    
        }
        """)
    
    def generate_password(self) -> None:
        symbols = string.punctuation.replace('"', '').replace("'", "").replace("\\", "")
        elements = string.ascii_letters + string.digits + symbols
        
        new_pass = "".join(choice(elements) for _ in range(16)) 

        self.password_label.setText(new_pass)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PassGenerator()
    window.show()
    sys.exit(app.exec())