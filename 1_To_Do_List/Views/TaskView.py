from PyQt5.QtWidgets import (QWidget, QMainWindow, QPushButton, QLabel, QLineEdit,
                             QScrollArea, QVBoxLayout, QHBoxLayout, QCheckBox, QSizePolicy,
                             QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from ..Models.Task import Task
from ..Services.TaskService import TaskService

class TaskView(QWidget):
    delete_requested = pyqtSignal(str)
    update_requested = pyqtSignal(Task)

    def __init__(self, task: Task):
        # Configs
        super().__init__()
        self._task_id = task.task_id

        self.check_box = QCheckBox(self)
        self.title_label = QLabel(self, text=task.title)
        self.title_label.setWordWrap(True)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.edit_button = QPushButton(self, text="✏️")
        self.delete_button = QPushButton(self, text="❌")
        self.title_entry = QLineEdit(self)
        self.title_entry.setPlaceholderText("Enter a new title: ")
        self.title_entry.hide()

        # Signals and Controlls
        self.delete_button.clicked.connect(self.request_delete)
        self.edit_button.clicked.connect(self.update_mode)
        self.title_entry.returnPressed.connect(self.commit_update)
        

        self.initUI()
    
    
    def initUI(self) -> None:
        self.hbox_elements = QHBoxLayout()

        self.hbox_elements.addWidget(self.check_box)
        self.hbox_elements.addWidget(self.title_label, 1)
        self.hbox_elements.addWidget(self.title_entry, 1)
        self.hbox_elements.addWidget(self.edit_button)
        self.hbox_elements.addWidget(self.delete_button)

        self.setLayout(self.hbox_elements)

        self.setObjectName("task_view")
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
        self.delete_requested.emit(str(self._task_id))

    def update_mode(self):
        self.title_label.hide()
        self.check_box.hide()
        self.delete_button.hide()
        self.title_entry.setText(self.title_label.text())
        self.title_entry.show()
        self.title_entry.setFocus()
        self.edit_button.setText("💾")
        self.edit_button.clicked.disconnect(self.update_mode)
        self.edit_button.clicked.connect(self.commit_update)
    
    def commit_update(self):
        new_title = self.title_entry.text().strip().upper()

        if not new_title:
            QMessageBox.warning(self, "Warning", "Task title cannot be empty!")
            return

        if new_title:
            updated_task = Task(task_id=self._task_id, title=new_title)
            self.update_requested.emit(updated_task)
            self.title_label.setText(new_title)

        self.title_entry.hide()
        self.title_label.show()
        self.check_box.show()
        self.delete_button.show()
        self.edit_button.setText("✏️")
        self.edit_button.clicked.disconnect(self.commit_update)
        self.edit_button.clicked.connect(self.update_mode)


class MainScreen(QMainWindow):
    def __init__(self, t_service: TaskService):
        # Configs
        super().__init__()
        self.setWindowTitle("To-Do App")
        self.resize(650, 700)
        self.move(600, 150)
        self._t_service = t_service

        # Widgets
        self.title_label = QLabel(self, text="To-Do List 📝")
        self.task_entry = QLineEdit(self)
        self.task_entry.setPlaceholderText("Enter a Task:")
        self.add_button = QPushButton(self, text="Add")
        self.task_container = QWidget()
        self.task_scroll_area = QScrollArea(self)

        self.initUI()
    
    def initUI(self) -> None:
        central = QWidget()
        self.main_layout = QVBoxLayout()
        self.entry_elements = QHBoxLayout()
        self.tasks = QVBoxLayout()

        # UI Configs
        self.entry_elements.addWidget(self.task_entry)
        self.entry_elements.addWidget(self.add_button)
        self.task_container.setLayout(self.tasks)
        self.task_scroll_area.setWidget(self.task_container)
        self.task_scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.entry_elements)
        self.main_layout.addWidget(self.task_scroll_area)

        self.setCentralWidget(central)
        central.setLayout(self.main_layout)

        self.add_button.setCursor(Qt.PointingHandCursor)
        self.task_container.setObjectName("task_container")
        self.title_label.setObjectName("title_label")
        self.tasks.setContentsMargins(10, 5, 10, 5)
        self.tasks.setAlignment(Qt.AlignTop)

        self.add_button.clicked.connect(self.add_task)
        self.task_entry.returnPressed.connect(self.add_task)

        # CSS
        self.setStyleSheet("""
        QWidget {
            font-size: 30px;
            font-family: "Segoe UI";
            background-color: #212433;
            color: white;
        }

        QWidget#task_container {
            background-color: #13131C;
            border-radius: 10px;                  
        }
                           
        QWidget#task_view {
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

        self.load_tasks()
    
    def load_tasks(self) -> None:
        tasks = self._t_service.get_all_tasks()
        for i in reversed(range(self.tasks.count())):  # percorre de trás para frente
            item = self.tasks.itemAt(i)
            widget = item.widget()
            if widget:
                # Remove o widget do layout e marca para deleção
                self.tasks.takeAt(i)
                widget.setParent(None)
                widget.deleteLater()
        
        # Atualiza o container e o scroll
        self.task_container.updateGeometry()
        self.task_scroll_area.widget().adjustSize()
        self.task_scroll_area.update()

        for t in tasks:
            widget = TaskView(t)
            widget.delete_requested.connect(self.delete_task)
            widget.update_requested.connect(self.update_task)
            self.tasks.addWidget(widget)

    def add_task(self):
        try:
            task_title = self.task_entry.text().strip()

            if not task_title:
                raise ValueError("Enter a Task!")

            task = self._t_service.add_task(task_title)
            task_widget = TaskView(task)
            task_widget.delete_requested.connect(self.delete_task)
            task_widget.update_requested.connect(self.update_task)
            self.tasks.addWidget(task_widget, alignment=Qt.AlignTop)
            
            self.task_entry.clear()
        except Exception as e:
            QMessageBox.critical(self, "ERROR", str(e))
    
    def delete_task(self, task_id: str):
        confirm = QMessageBox.question(self, "Confirm Delete", 
                                       "Are you sure you want to delete this task?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm:
            success = self._t_service.delete_task(task_id)
            if success:
                for i in reversed(range(self.tasks.count())):
                    widget = self.tasks.itemAt(i).widget()
                    if getattr(widget, "_task_id", None) == task_id:
                        widget.setParent(None)
                        widget.deleteLater()
                        break
                
                self.load_tasks()
            else:
                QMessageBox.critical(self, "ERROR", "Could not delete task!")
    
    def update_task(self, updated_task: Task):
        success = self._t_service.update_task(updated_task)
        if not success:
            QMessageBox.critical(self, "ERROR", "Could not update task!")
