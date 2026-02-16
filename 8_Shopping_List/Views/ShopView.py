from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QScrollArea, QCheckBox, QSizePolicy, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from ..Services.ShopService import ShopService
from ..Models.Shopping import Shopping

class ShopView(QWidget):
    delete_requested = pyqtSignal(str)
    update_requested = pyqtSignal(Shopping)

    def __init__(self, shop: Shopping):
        # Configs
        super().__init__()
        self._shop_id = shop.shop_id
        self._name = shop.name
        self._quantity = shop.quantity

        self.check_box = QCheckBox(self)
        self.title_label = QLabel(self, text=shop.__str__())
        self.title_label.setWordWrap(True)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.edit_button = QPushButton(self, text="✏️")
        self.delete_button = QPushButton(self, text="❌")
        self.name_entry = QLineEdit(self)
        self.name_entry.setPlaceholderText("Enter a new name: ")
        self.name_entry.hide()
        self.quantity_entry = QLineEdit(self)
        self.quantity_entry.setPlaceholderText("Enter a new quantity: ")
        self.quantity_entry.hide()

        # Signals and Controlls
        self.delete_button.clicked.connect(self.request_delete)
        self.edit_button.clicked.connect(self.update_mode)
        self.name_entry.returnPressed.connect(self.commit_update)
        self.quantity_entry.returnPressed.connect(self.commit_update)
        

        self.initUI()
    
    
    def initUI(self) -> None:
        self.hbox_elements = QHBoxLayout()

        self.hbox_elements.addWidget(self.check_box)
        self.hbox_elements.addWidget(self.title_label, 1)
        self.hbox_elements.addWidget(self.name_entry, 1)
        self.hbox_elements.addWidget(self.quantity_entry, 1)
        self.hbox_elements.addWidget(self.edit_button)
        self.hbox_elements.addWidget(self.delete_button)

        self.setLayout(self.hbox_elements)

        self.setObjectName("shop_view")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.title_label.setStyleSheet("background-color: transparent;")
        self.edit_button.setCursor(Qt.PointingHandCursor)
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.title_label.setAlignment(Qt.AlignVCenter)
        self.check_box.stateChanged.connect(self.toggle_done)
    
    def toggle_done(self, state) -> None:
        if state == Qt.Checked:
            self.title_label.setStyleSheet("""
                color: #888;
                text-decoration: line-through;
                background-color: transparent;
            """)
        else:
            self.title_label.setStyleSheet("""
                color: white;
                text-decoration: none;
                background-color: transparent;
            """)

    def request_delete(self):
        self.delete_requested.emit(str(self._shop_id))

    def update_mode(self):
        self.title_label.hide()
        self.check_box.hide()
        self.delete_button.hide()
        self.name_entry.setText(self._name)
        self.name_entry.show()
        self.quantity_entry.setText(str(self._quantity))
        self.quantity_entry.show()
        self.name_entry.setFocus()
        self.edit_button.setText("💾")
        self.edit_button.clicked.disconnect(self.update_mode)
        self.edit_button.clicked.connect(self.commit_update)
    
    def commit_update(self):
        try:
            new_name = self.name_entry.text().strip().upper()
            new_quantity = int(self.quantity_entry.text().strip())
        except Exception as e:
            QMessageBox.critical(self, "ERROR", "Invalid data")
            return

        if not new_name or not new_quantity:
            QMessageBox.warning(self, "Warning", "Fields cannot be empty!")
            return

        updated_shop = Shopping(shop_id=self._shop_id, name=new_name, quantity=new_quantity)
        self.update_requested.emit(updated_shop)
        self.title_label.setText(f"Name: {new_name} | Quantity: {new_quantity}")
        self._name = new_name
        self._quantity = new_quantity

        self.name_entry.hide()
        self.quantity_entry.hide()
        self.title_label.show()
        self.check_box.show()
        self.delete_button.show()
        self.edit_button.setText("✏️")
        self.edit_button.clicked.disconnect(self.commit_update)
        self.edit_button.clicked.connect(self.update_mode)


class MainWindow(QMainWindow):
    def __init__(self, s_service: ShopService):
        # Configs
        super().__init__()
        self.setWindowTitle("Shop List")
        self.resize(650, 700)
        self.move(600, 150)
        self._shop_service = s_service

        # Widgets
        self.title_label = QLabel(self, text="Shop List 📝")
        self.name_entry = QLineEdit(self)
        self.name_entry.setPlaceholderText("Enter a shop name:")
        self.quantity_entry = QLineEdit(self)
        self.quantity_entry.setPlaceholderText("Enter a shop quantity:")
        self.add_button = QPushButton(self, text="Add")
        self.shop_container = QWidget()
        self.shop_scroll_area = QScrollArea(self)

        self.initUI()
    
    def initUI(self) -> None:
        central = QWidget()
        self.main_layout = QVBoxLayout()
        self.entry_elements = QHBoxLayout()
        self.shops = QVBoxLayout()

        # UI Configs
        self.entry_elements.addWidget(self.name_entry)
        self.entry_elements.addWidget(self.quantity_entry)
        self.entry_elements.addWidget(self.add_button)
        self.shop_container.setLayout(self.shops)
        self.shop_scroll_area.setWidget(self.shop_container)
        self.shop_scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.entry_elements)
        self.main_layout.addWidget(self.shop_scroll_area)

        self.setCentralWidget(central)
        central.setLayout(self.main_layout)

        self.add_button.setCursor(Qt.PointingHandCursor)
        self.shop_container.setObjectName("shop_container")
        self.title_label.setObjectName("title_label")
        self.shops.setContentsMargins(10, 5, 10, 5)
        self.shops.setAlignment(Qt.AlignTop)

        self.add_button.clicked.connect(self.add_shop)
        self.name_entry.returnPressed.connect(self.add_shop)
        self.quantity_entry.returnPressed.connect(self.add_shop)

        # CSS
        self.setStyleSheet("""
        QWidget {
            font-size: 30px;
            font-family: "Segoe UI";
            background-color: #212433;
            color: white;
        }

        QWidget#shop_container {
            background-color: #13131C;
            border-radius: 10px;                  
        }
                           
        QWidget#shop_view {
            background-color: #24242B;
            border-radius: 12px;
            max-height: 100px;
            padding: 8px;                   
        }
                           
        QLabel#title_label {
            font-size: 50px;
            margin: 5px;                 
        }

        QLineEdit {
            background-color: #EBEBEB;
            color: black;
            padding: 10px;
            border-radius: 32px;       
            margin: 15px;
        }
        
        QLineEdit:focus {
            border: 3px solid #272DC2;                 
        }

        QPushButton {
            background-color: #272DC2;
            padding: 12px 16px;
            border-radius: 20px;                   
        }

        QPushButton:hover {
            background-color: #4449E3;                   
        }
                           
        QCheckBox::indicator {
            width: 28px;
            height: 28px;
            border-radius: 6px;
        }

        QCheckBox::indicator:unchecked {
            border: 2px solid white;
            background-color: white;
        }
                           
        QCheckBox::indicator:checked {
            background-color: #272DC2;
            border: 2px solid #272DC2;
        }
        """)

        self.load_shops()
    
    def load_shops(self) -> None:
        shops = self._shop_service.get_all_shops()
        for i in reversed(range(self.shops.count())):
            item = self.shops.itemAt(i)
            widget = item.widget()
            if widget:
                self.shops.takeAt(i)
                widget.setParent(None)
                widget.deleteLater()
        
        self.shop_container.updateGeometry()
        self.shop_scroll_area.widget().adjustSize()
        self.shop_scroll_area.update()

        for s in shops:
            widget = ShopView(s)
            widget.delete_requested.connect(self.delete_shop)
            widget.update_requested.connect(self.update_shop)
            self.shops.addWidget(widget)
    
    def add_shop(self) -> None:
        try:
            shop_name = self.name_entry.text().strip()
            quantity = int(self.quantity_entry.text().strip())

            if not shop_name or not quantity:
                raise ValueError("Enter a valid shop data")

            shop = self._shop_service.add_shop(shop_name, quantity)
            shop_widget = ShopView(shop)
            shop_widget.delete_requested.connect(self.delete_shop)
            shop_widget.update_requested.connect(self.update_shop)
            self.shops.addWidget(shop_widget, alignment=Qt.AlignTop)
            
            self.name_entry.clear()
            self.quantity_entry.clear()
        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))
    
    def delete_shop(self, shop_id: str):
        confirm = QMessageBox.question(self, "Confirm Delete", 
                                       "Are you sure you want to delete this shop?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            success = self._shop_service.delete_shop(shop_id)
            if success:
                for i in reversed(range(self.shops.count())):
                    widget = self.shops.itemAt(i).widget()
                    if getattr(widget, "_shop_id", None) == shop_id:
                        widget.setParent(None)
                        widget.deleteLater()
                        break
                
                self.load_shops()
            else:
                QMessageBox.critical(self, "ERROR", "Could not delete shop!")
    
    def update_shop(self, updated_shop: Shopping) -> None:
        success = self._shop_service.update_shop(updated_shop)
        if not success:
            QMessageBox.critical(self, "ERROR", "Could not update Shop!")
        