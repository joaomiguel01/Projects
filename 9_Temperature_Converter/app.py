from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
import sys

class MainApp(QWidget):
    def __init__(self):
        # Widgets
        super().__init__()
        self.setWindowTitle("Temperature Converter")
        self.setFixedSize(600, 400)
        self.move(700, 300)

        # Widgets
        self.temp_entry = QLineEdit(self)
        self.temp_entry.setPlaceholderText("Enter a temperature")
        self.display_label = QLabel(self)
        self.entry_combo = QComboBox(self)
        self.entry_combo.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        self.display_combo = QComboBox(self)
        self.display_combo.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        self.convert_button = QPushButton(self, text="Convert")

        self.initUI()
    
    def initUI(self) -> None:
        # Layouts
        self.main_layout = QVBoxLayout()
        self.fields_layout = QHBoxLayout()
        self.combo_layout = QHBoxLayout()

        self.fields_layout.addWidget(self.temp_entry)
        self.fields_layout.addWidget(self.display_label)
        self.combo_layout.addWidget(self.entry_combo)
        self.combo_layout.addWidget(self.display_combo)

        self.main_layout.addLayout(self.fields_layout)
        self.main_layout.addLayout(self.combo_layout)
        self.main_layout.addWidget(self.convert_button, alignment=Qt.AlignCenter)

        self.setLayout(self.main_layout)

        # UI Configs
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        self.temp_entry.setAlignment(Qt.AlignCenter)
        self.display_label.setAlignment(Qt.AlignCenter)
        self.convert_button.setCursor(Qt.PointingHandCursor)
        self.entry_combo.setCursor(Qt.PointingHandCursor)
        self.display_combo.setCursor(Qt.PointingHandCursor)

        # CSS
        self.setStyleSheet("""
        QWidget {
            background-color: #1E151F;
            font-size: 20px;
            font-family: Segoe UI;           
        }
                           
        QLineEdit {
            background-color: white;
            border: 2px solid #753BA8;
            border-radius: 10px;
            max-width: 200px;
            margin-right: 50px;
            font-size: 30px;
            padding: 5px;                
        }
                           
        QLabel {
            background-color: white;
            border: 2px solid #753BA8;
            border-radius: 10px;
            max-width: 200px;
            max-height: 45px;
            margin-left: 50px;
            font-size: 30px;
            padding: 5px; 
        }
                           
        QComboBox {
            background-color: blue;
            max-width: 200px;
            font-size: 30px;
            color: white;
            margin: 40px;
            padding: 5px;
        }
                           
        QPushButton {
            background-color: #FCA819;
            padding: 20px;
            font-size: 25px;
            font-weight: bold;
            max-width: 200px;
            border-radius: 30px;                  
        }
                           
        QPushButton:hover {
            background-color: #FFC45C;                   
        }
        """)

        # Control Config
        self.convert_button.clicked.connect(self.convert_temp)
    
    def convert_temp(self) -> None:
        
        try:
            temp = float(self.temp_entry.text().strip().replace(",", "."))
            from_temp = self.entry_combo.currentText().upper()
            to_temp = self.display_combo.currentText().upper()

            if to_temp == "CELSIUS":
                if from_temp == "FAHRENHEIT":
                    self.display_label.setText(f"{(temp - 32) * 5 / 9:.2f}")
                elif from_temp == "KELVIN":
                    self.display_label.setText(f"{temp-273.15:.2f}")
                else:
                    self.show_errors("Cannot convert to the same unit!")
            elif to_temp == "FAHRENHEIT":
                if from_temp == "CELSIUS":
                    self.display_label.setText(f"{(temp*9/5)+32:.2f}")
                elif from_temp == "KELVIN":
                    self.display_label.setText(f"{(temp-273.15)*9/5+32:.2f}")
                else:
                    self.show_errors("Cannot convert to the same unit!")
            elif to_temp == "KELVIN":
                if from_temp == "CELSIUS":
                    self.display_label.setText(f"{temp+273.15:.2f}")
                elif from_temp == "FAHRENHEIT":
                    self.display_label.setText(f"{(temp-32)*5/9+273.15:.2f}")
                else:
                    self.show_errors("Cannot convert to the same unit!")
        except ValueError:
            self.show_errors("Enter a valid number!")
        except Exception as e:
            self.show_errors(str(e))
    
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