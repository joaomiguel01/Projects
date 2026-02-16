from PyQt5.QtWidgets import (QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton,
                             QApplication, QLabel, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
import sys
import requests


class Converter(QWidget):
    def __init__(self):
        # Configs
        super().__init__()
        self.setWindowTitle("Currency Converter")
        self.setFixedSize(600, 400)
        self.move(700, 300)

        # Widgets
        self.currency_entry = QLineEdit(self)
        self.currency_entry.setPlaceholderText("Enter a value")
        self.response_label = QLabel(self)
        self.entry_combo = QComboBox(self)
        self.entry_combo.addItems(["USD", "BRL", "EUR", "GBP"])
        self.response_combo = QComboBox(self)
        self.response_combo.addItems(["USD", "BRL", "EUR", "GBP"])
        self.converter_button = QPushButton(self, text="Convert")

        self.initUI()
    
    def initUI(self) -> None:
        self.main_layout = QVBoxLayout()
        self.display_layout = QHBoxLayout()
        self.combo_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.display_layout.addWidget(self.currency_entry)
        self.display_layout.addWidget(self.response_label)
        self.combo_layout.addWidget(self.entry_combo)
        self.combo_layout.addWidget(self.response_combo)

        self.main_layout.addLayout(self.display_layout)
        self.main_layout.addLayout(self.combo_layout)
        self.main_layout.addWidget(self.converter_button, alignment=Qt.AlignCenter)

        self.setLayout(self.main_layout)


        # UI Configs
        self.response_label.setAlignment(Qt.AlignCenter)
        self.converter_button.setCursor(Qt.PointingHandCursor)
        self.entry_combo.setCursor(Qt.PointingHandCursor)
        self.response_combo.setCursor(Qt.PointingHandCursor)
        self.converter_button.clicked.connect(self.converter_fuction)

        # CSS
        self.setStyleSheet("""
        QWidget{
            background-color: #362832;
            font-family: Segoe UI;                   
        }
        
        QLineEdit{
            background-color: white;
            border: none;
            border-radius: 5px;
            font-size: 30px;
            max-width: 200px;
            margin-right: 100px;                   
        }
                           
        QLabel{
            background-color: white;
            max-width: 200px;
            max-height: 45px;
            border-radius: 5px;
            font-size: 30px;
            border: none;                   
        }

        QComboBox{
            background-color: orange;
            max-width: 200px;
            margin: 20px;
            font-size: 25px;
            border-radius: 5px;                   
        }
                                  
        QPushButton{
            background-color: #5372E6;
            max-width: 200px;
            font-size: 30px;
            padding: 10px;
            border-radius: 10px;            
        }
                           
        QPushButton:hover{
            background-color: #8099ED;                    
        }
        """)
    
    def converter_fuction(self) -> None:
        try:
            amount = float(self.currency_entry.text())
            from_currency = self.entry_combo.currentText()
            to_currency = self.response_combo.currentText()
            API_URL = f"https://api.frankfurter.app/latest"
            params = {
                "amount": amount,
                "from": from_currency,
                "to": to_currency
            }

            response = requests.get(API_URL, params=params)
            data = response.json()

            self.response_label.setText(f"{data['rates'][to_currency]:.2f}")
        except Exception as e:
            self.show_error(str(e))
    
    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("ERROR")
        msg.setText(message)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #362832;
                color: black;
                font-size: 14px;
            }
            QLabel {
                color: black;
                font-size: 16px;
            }
            QPushButton {
                background-color: #5372E6;
                padding: 6px;
                border-radius: 6px;
                color: white;
            }
            QPushButton:hover {
                background-color: #8099ED;
            }
        """)

        msg.exec_()

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Converter()
    window.show()
    sys.exit(app.exec())