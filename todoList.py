"""To-Do List
Program made by: Henrique Pinho and Isaac Cisneros
Sources: https://doc.qt.io/qtforpython-6/
Warmup B-> shopping list

Functions of the program: Lets the user manage his tasks in a simple and effective way

First draft: 12/01/2023
Last draft 12/12/2023

OBS: We were not able to write many doctests because most of our program is related to visual things and text
files, so wrtitng tests for them would mess up the program itself
"""


import os
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QAbstractItemView, QComboBox,
    QTableWidgetItem, QDateEdit, QDialog, QMessageBox, QTableWidget
)

class LoginDialog(QDialog):
    def __init__(self, user_credentials_file='user_credentials.txt'):
        super().__init__()

        self.user_credentials_file = user_credentials_file

        self.setWindowTitle("Login")
        layout = QVBoxLayout()

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        layout.addWidget(self.username_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.setLayout(layout)

        # Create the user credentials file if it doesn't exist
        if not os.path.exists(self.user_credentials_file):
            with open(self.user_credentials_file, 'w'):
                pass

    def register(self):
        """Register a new user
        
        Checks if username exists, and registers user if valid
        
        >>> self.register("", "")
        False
        >>> self.register("test", "1234")
        True
        >>> self.username_exists("test")
        True
        """
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            QMessageBox.warning(self, "Incomplete Fields", "Username and password are required.")
            return

        if self.username_exists(username):
            QMessageBox.warning(self, "Username Exists", "Username already exists. Please choose another.")
            return

        with open(self.user_credentials_file, "a") as f:
            f.write(f"{username}|{password}\n")
            QMessageBox.information(self, "Registration Successful", "Account created successfully.")

    def login(self):
        
        
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            QMessageBox.warning(self, "Incomplete Fields", "Username and password are required.")
            return

        with open(self.user_credentials_file, "r") as f:
            for line in f:
                stored_username, stored_password = map(str.strip, line.split('|'))
                if username == stored_username and password == stored_password:
                    self.accept()  # Close the dialog
                    return

        QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def username_exists(self, username):
        #Check if a username already exists in the credentials file
        with open(self.user_credentials_file, "r") as f:
            for line in f:
                stored_username, _ = map(str.strip, line.split('|'))
                if username == stored_username:
                    return True
        return False

class ToDoList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do list!")
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        label = QLabel("TO-DO LIST")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.task = QLineEdit()
        self.task.setPlaceholderText("Task")
        layout1.addWidget(self.task)

        self.deadline = QDateEdit(QDate(2023, 12, 13), self)
        self.deadline.setDisplayFormat("MM/dd/yyyy")
        self.deadline.setCalendarPopup(True)
        layout1.addWidget(self.deadline)

        layout.addLayout(layout1)

        self.details = QLineEdit()
        self.details.setPlaceholderText("Details")
        layout2.addWidget(self.details)

        self.priorities = QComboBox()
        self.priorities.setPlaceholderText("Choose One")
        self.priorities.addItem("High")
        self.priorities.addItem("Medium")
        self.priorities.addItem("Low")
        layout2.addWidget(self.priorities)

        layout.addLayout(layout2)

        addButton = QPushButton("Add!")
        addButton.clicked.connect(self.additem)
        self.task.returnPressed.connect(self.additem)
        layout.addWidget(addButton)

        self.todo_list = QTableWidget(self)
        self.todo_list.setColumnCount(4)
        self.todo_list.setHorizontalHeaderLabels(['Task', 'Details', 'Priority', 'Deadline'])
        self.todo_list.setSortingEnabled(True)

        path = 'myfile.txt'
        if os.path.exists(path):
            with open("myfile.txt", "r") as f:
                for line in f:
                    task, details, priority, deadline = map(str.strip, line.split('|'))

                    colors = {"Low": "green", "Medium": "yellow", "High": "red"}

                    row_item_task = QTableWidgetItem(task)
                    row_item_details = QTableWidgetItem(details)
                    row_item_priority = QTableWidgetItem(priority)
                    row_item_deadline = QTableWidgetItem(deadline)

                    self.todo_list.insertRow(self.todo_list.rowCount())
                    self.todo_list.setItem(self.todo_list.rowCount() - 1, 0, row_item_task)
                    self.todo_list.setItem(self.todo_list.rowCount() - 1, 1, row_item_details)
                    self.todo_list.setItem(self.todo_list.rowCount() - 1, 2, row_item_priority)
                    self.todo_list.setItem(self.todo_list.rowCount() - 1, 3, row_item_deadline)

                    row_item_task.setForeground(QColor(colors[priority]))
                    row_item_details.setForeground(QColor(colors[priority]))
                    row_item_priority.setForeground(QColor(colors[priority]))
                    row_item_deadline.setForeground(QColor(colors[priority]))

        self.todo_list.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.todo_list)

        removeButton = QPushButton("Remove!")
        removeButton.clicked.connect(self.removeitem)
        layout.addWidget(removeButton)
        
        saveButton = QPushButton("Save Edits")
        saveButton.clicked.connect(self.saveToFile)
        layout.addWidget(saveButton)

        widget = QWidget()
        widget.setLayout(layout)
        self.setGeometry(500, 300, 500, 500)
        self.setCentralWidget(widget)

    def additem(self):
        #Add a new item to the to-do list
        if not self.deadline.date().isValid():
            QMessageBox.warning(self, "Invalid Date", "Invalid date format. Please use mm/dd/yyyy.")
            self.deadline.clear()
        elif not self.task.text() or not self.priorities.currentText():
            QMessageBox.warning(self, "Incomplete Fields", "Task and Priority are required fields.")
        else:
            task_text = self.task.text()
            details_text = self.details.text() if self.details.text() else ""
            priority_text = self.priorities.currentText()
            deadline_text = self.deadline.date().toString("MM/dd/yyyy")

            # Add separator '|' between task, details, priority, and deadline
            line = f"{task_text}|{details_text}|{priority_text}|{deadline_text}\n"

            with open("myfile.txt", "a") as f:
                f.write(line)

            row_position = self.todo_list.rowCount()

            task = QTableWidgetItem(task_text)
            deadline = QTableWidgetItem(deadline_text)
            details = QTableWidgetItem(details_text)
            priority = QTableWidgetItem(priority_text)

            colors = {"Low": "green", "Medium": "yellow", "High": "red"}

            if priority_text == 'High':
                task.setForeground(QColor('red'))
                deadline.setForeground(QColor('red'))
                details.setForeground(QColor('red'))
                priority.setForeground(QColor('red'))
            elif priority_text == 'Medium':
                task.setForeground(QColor('orange'))
                deadline.setForeground(QColor('orange'))
                details.setForeground(QColor('orange'))
                priority.setForeground(QColor('orange'))
            elif priority_text == 'Low':
                task.setForeground(QColor('green'))
                deadline.setForeground(QColor('green'))
                details.setForeground(QColor('green'))
                priority.setForeground(QColor('green'))

            self.todo_list.insertRow(row_position)
            self.todo_list.setItem(row_position, 0, task)
            self.todo_list.setItem(row_position, 1, details)
            self.todo_list.setItem(row_position, 2, priority)
            self.todo_list.setItem(row_position, 3, deadline)

            self.task.setText("")
            self.deadline.clear()
            self.details.setText("")
            self.priorities.setCurrentIndex(-1)

    def removeitem(self):
        #Remove selected items from the to-do list
        selected_rows = set()
        for index in self.todo_list.selectedIndexes():
            selected_rows.add(index.row())

        if not selected_rows:
            return

        confirmation_text = "Remember to click save edits before closing the list! This will delete the entire row of the items selected. Are you sure you want to do that? "
        user_confirmation = QMessageBox.question(self, "Confirm Deletion", confirmation_text, QMessageBox.Yes | QMessageBox.No)

        if user_confirmation == QMessageBox.No:
            return

        with open('myfile.txt', 'r') as f:
            lines = f.readlines()

        with open('myfile.txt', 'w') as f:
            for i, line in enumerate(lines):
                if i // 4 not in selected_rows:
                    f.write(line)

        for row in selected_rows:
            self.todo_list.removeRow(row)
            
    def saveToFile(self):
        #Save the current to-do list content to a file
        string = ''
        for row in range(self.todo_list.rowCount()):
            for column in range(self.todo_list.columnCount()):
                cell_item = self.todo_list.item(row, column)
                string += cell_item.text() + '|'
            string = string.rstrip('|') + '\n'  # Remove the trailing '|' and add a newline
        with open('myfile.txt', 'w') as f:
            f.write(string)

         
if __name__ == "__main__":
    app = QApplication()
    import doctest
    doctest.testmod()
    # Show login dialog as a pop-up
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        # If login is successful, show the to-do list window
        main_window = ToDoList()
        main_window.show()

    app.exec()
