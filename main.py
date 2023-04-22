from PyQt5.QtWidgets import *
from dashboard import DashboardWidget
from calendar_view import CalendarWidget

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        dashboard = DashboardWidget(self)
        calendar_widget = CalendarWidget(dashboard, self)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(calendar_widget)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
