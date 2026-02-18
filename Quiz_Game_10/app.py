from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton,
                             QLabel, QMainWindow, QButtonGroup, QMessageBox)
from PyQt5.QtCore import Qt
from .db import questions, responses, options
import sys

class MainApp(QMainWindow):
    def __init__(self):
        # Configs
        super().__init__()
        self.setWindowTitle("Quiz Game")
        self.setFixedSize(700, 500)
        self.move(650, 250)
        self.question_number = 0
        self.score = 0

        # Widgets
        self.question_label = QLabel(self, text=f"{self.question_number+1}. {questions[self.question_number]}")
        self.elements_container = QWidget()
        self.radio1 = QRadioButton(self, text=f"{options[self.question_number][0]}")
        self.radio2 = QRadioButton(self, text=f"{options[self.question_number][1]}")
        self.radio3 = QRadioButton(self, text=f"{options[self.question_number][2]}")
        self.radio4 = QRadioButton(self, text=f"{options[self.question_number][3]}")
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.radio1, 0)
        self.radio_group.addButton(self.radio2, 1)
        self.radio_group.addButton(self.radio3, 2)
        self.radio_group.addButton(self.radio4, 3)
        self.confirm_button = QPushButton(self, text="Confirm")

        self.initUI()
    
    def initUI(self) -> None:
        # Layouts
        self.main_layout = QVBoxLayout()
        self.radio_layout = QVBoxLayout()

        self.radio_layout.addWidget(self.radio1)
        self.radio_layout.addWidget(self.radio2)
        self.radio_layout.addWidget(self.radio3)
        self.radio_layout.addWidget(self.radio4)
        
        self.main_layout.addWidget(self.question_label)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.radio_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.confirm_button, alignment=Qt.AlignRight)

        self.elements_container.setLayout(self.main_layout)
        self.setCentralWidget(self.elements_container)

        # UI Configs
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.question_label.setWordWrap(True)
        self.confirm_button.setCursor(Qt.PointingHandCursor)

        # CSS
        self.setStyleSheet("""
        QWidget {
            background-color: #f2f2f2;
            font-family: Segoe UI;
        }

        QFrame {
            background-color: white;
            border-radius: 20px;
            padding: 25px;
        }

        QLabel {
            font-size: 30px;
            font-weight: bold;
            color: #222;                 
        }
                           
        QRadioButton {
            font-size: 24px;
            padding: 10px;
            border-radius: 10px;
            margin-left: 30px;
        }
                           
        QRadioButton:hover {
            background-color: #e8e8e8;
        }
                           
        QPushButton {
            background-color: #0078d7;
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 12px 25px;
            border-radius: 15px;
        }
                           
        QPushButton:hover {
            background-color: #005fa3;
        }
        """)
    
        # Control Config
        self.confirm_button.clicked.connect(self.confirm_response)

    def confirm_response(self) -> None:
        confirm = QMessageBox.question(self, "Confirmation", "Are you sure about your answer?",
                             QMessageBox.Yes, QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            letters = ["A", "B", "C", "D"]

            radio_id = self.radio_group.checkedId()

            if letters[radio_id] == responses[self.question_number]:
                self.score += 10
                QMessageBox.information(self, "CONGRATULATIONS!", "CORRECT Answer!")
            elif radio_id == -1:
                self.show_errors("Select a valid option!")
                return
            else:
                QMessageBox.information(self, "BOOOOOOO!", "INCORRET Answer!")
            
            self.question_number += 1
            if self.question_number >= len(questions):
                self.close()
                QMessageBox.information(self, "Quiz Finished", f"Your final score is {self.score}/100")
            else:
                self.update_display()
    
    def update_display(self) -> None:
        self.question_label.setText(f"{self.question_number+1}. {questions[self.question_number]}")
        self.radio1.setText(f"{options[self.question_number][0]}")
        self.radio2.setText(f"{options[self.question_number][1]}")
        self.radio3.setText(f"{options[self.question_number][2]}")
        self.radio4.setText(f"{options[self.question_number][3]}")

        self.radio_group.setExclusive(False)
        self.radio1.setChecked(False)
        self.radio2.setChecked(False)
        self.radio3.setChecked(False)
        self.radio4.setChecked(False)
        self.radio_group.setExclusive(True)
    
    def show_errors(self, text: str) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("ERROR!")
        msg.setText(text)

        msg.setStyleSheet("""
        QMessageBox {
            background-color: #1e1e1e;
            color: white;
            font-size: 14px;                  
        }
                          
        QLabel {
            color: white;
            font-size: 25px;
        }
                          
        QPushButton {
            background-color: #ff4444;
            color: white;
            padding: 6px 15px;
            border-radius: 8px;
        }
                          
        QPushButton:hover {
            background-color: #cc0000;
        }
        """)

        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())