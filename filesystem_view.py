from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class FileSystemView(QWidget):
    def __init__(self, dir_path):
        super().__init__()

        appWidth = 800
        appHeight = 600

        self.setWindowTitle("File System View")
        self.setGeometry(300, 300, appWidth, appHeight)

        self.model = QFileSystemModel()
        self.model.setRootPath(dir_path)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(dir_path))
        self.tree.setColumnWidth(0, 250)
        self.tree.setAlternatingRowColors(True)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)

        self.setLayout(layout)
