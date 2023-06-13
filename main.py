from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import QDate, Qt
from dashboard import DashboardWidget
from calendar_view import CalendarWidget
from alertView import Notification, init, Urgency, onClose, onHelp, onIgnore


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        dashboard = DashboardWidget(self)
        calendar_widget = CalendarWidget(dashboard, self)

        dt = QDate.currentDate()
        calendar_widget.update_special_events(dt)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(calendar_widget)
        self.setLayout(self.layout)
        init("demo")
        for event in calendar_widget.events:
            if event['date'] == dt.toString(Qt.ISODate):
                n = Notification(f"Your daily notification: ", "Today is " +
                                 dt.toString(Qt.ISODate) + "\nYor event: " + event['title'], timeout=3000)
                n.setUrgency(Urgency.NORMAL)
                n.setCategory("device")
                n.setIconPath(
                    "/usr/share/icons/Tango/scalable/status/dialog-error.svg")
                n.addAction("help", "Help", onHelp)
                n.addAction("ignore", "Ignore", onIgnore, 12345)
                n.onClosed(onClose)
                n.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)
        self.showMaximized()


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
