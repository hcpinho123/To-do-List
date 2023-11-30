'''Henrique Pinho
Date I did it: 11/09/2023
sources: https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QListWidget.html#
'''

import os 

from PySide6.QtWidgets import \
     QApplication, QMainWindow, QVBoxLayout, QWidget, \
     QLabel, QLineEdit, QPushButton, QListWidget, QAbstractItemView


class shoppingList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shopping List!")
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Shopping List"))
        
        self.item = QLineEdit()
        self.item.setPlaceholderText("item")
        layout.addWidget(self.item)
        
#         self.quantity = QLineEdit()
#         self.quantity.setPlaceholderText("Quantity of items")
#         layout.addWidget(self.quantity)
#         
#         self.expDate = QLineEdit()
#         self.expDate.setPlaceholderText("Expiration Day")
#         layout.addWidget(self.expDate)
        
        addButton = QPushButton("Add!")
        addButton.clicked.connect(self.additem)
        self.item.returnPressed.connect(self.additem)
        layout.addWidget(addButton)
        
        removeButton = QPushButton("Remove!")
        removeButton.clicked.connect(self.removeitem)
        layout.addWidget(removeButton)
        
        self.shopping_list = QListWidget(self)
        self.shopping_list.setSortingEnabled(True)
        
        path = 'myfile.txt'
        if os.path.exists(path):
            f = open("myfile.txt", "r")
            for i in f.readlines():
                self.shopping_list.addItem(i)
                f.close()
        
        self.shopping_list.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(self.shopping_list)

        
        # add layout to window
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def additem(self):
        self.shopping_list.addItem(self.item.text())
        f = open("myfile.txt", "a")
        f.write(self.item.text())
        f.write('\n')
        f.close()
        self.item.setText("")
                    
    def removeitem(self):
        selected_items = self.shopping_list.selectedItems()

        if not selected_items:
            return

        with open('myfile.txt', 'r') as f:
            lines = f.readlines()

        with open('myfile.txt', 'w') as f:
            for line in lines:
                if line.strip() + '\n' not in [item.text() for item in selected_items]:
                    f.write(line)

        for item in selected_items:
            self.shopping_list.takeItem(self.shopping_list.row(item))
        
if __name__ == "__main__":
    app = QApplication()
    window = shoppingList()
    window.show()
    app.exec()
