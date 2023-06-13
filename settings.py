from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from settings_manager import SettingsManager


class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.color_label = QLabel("Wybierz kolor tła kalendarza:")
        self.color_combo_box = QComboBox()
        self.color_combo_box.addItem("Niebieski")
        self.color_combo_box.addItem("Beżowy")
        self.color_combo_box.addItem("Czerwony")
        self.color_combo_box.addItem("Pomarańczowo-żółty")
        self.color_combo_box.addItem("Różowy")
        self.color_combo_box.addItem("Fioletowy")

        self.filters_label = QLabel("Wybierz filtry:")
        self.filters_combo_box = QComboBox()
        self.filters_combo_box.addItem("Urodziny")
        self.filters_combo_box.addItem("Imieniny")
        self.filters_combo_box.addItem("Święta")
        self.filters_combo_box.addItem("Kulturalne")
        self.filters_combo_box.addItem("Biznesowe")
        self.filters_combo_box.addItem("Naukowe")
        self.filters_combo_box.addItem("Inne")

        self.birthday_label = QLabel("Urodziny:")
        self.birthdays_checkbox = QCheckBox("Urodziny")
        self.birthdays_checkbox.setChecked(True)
        self.name_day_label = QLabel("Imieniny:")
        self.name_day_checkbox = QCheckBox("Imieniny")
        self.name_day_checkbox.setChecked(True)
        self.holiday_label = QLabel("Święta:")
        self.holiday_checkbox = QCheckBox("Święta")
        self.holiday_checkbox.setChecked(True)
        self.cultural_label = QLabel("Kulturalne:")
        self.cultural_checkbox = QCheckBox("Kulturalne")
        self.cultural_checkbox.setChecked(True)
        self.business_label = QLabel("Biznesowe:")
        self.business_checkbox = QCheckBox("Biznesowe")
        self.business_checkbox.setChecked(True)
        self.scientific_label = QLabel("Naukowe:")
        self.scientific_checkbox = QCheckBox("Naukowe")
        self.scientific_checkbox.setChecked(True)
        self.other_label = QLabel("Inne:")
        self.other_checkbox = QCheckBox("Inne")
        self.other_checkbox.setChecked(True)

        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color_combo_box)
        self.layout.addWidget(self.filters_label)
        self.layout.addWidget(self.filters_combo_box)
        self.layout.addWidget(self.birthday_label)
        self.layout.addWidget(self.birthdays_checkbox)
        self.layout.addWidget(self.name_day_label)
        self.layout.addWidget(self.name_day_checkbox)
        self.layout.addWidget(self.holiday_label)
        self.layout.addWidget(self.holiday_checkbox)
        self.layout.addWidget(self.cultural_label)
        self.layout.addWidget(self.cultural_checkbox)
        self.layout.addWidget(self.business_label)
        self.layout.addWidget(self.business_checkbox)
        self.layout.addWidget(self.scientific_label)
        self.layout.addWidget(self.scientific_checkbox)
        self.layout.addWidget(self.other_label)
        self.layout.addWidget(self.other_checkbox)

        self.setLayout(self.layout)

    def get_selected_color(self):
        color_name = self.color_combo_box.currentText()
        if color_name == "Beżowy":
            return QColor(255, 255, 240)
        elif color_name == "Niebieski":
            return QColor(219, 244, 255)
        elif color_name == "Czerwony":
            return QColor(255, 219, 219)
        elif color_name == "Pomarańcszo-żółty":
            return QColor(255, 247, 219)
        elif color_name == "Różowy":
            return QColor(255, 235, 254)
        elif color_name == "Fioletowy":
            return QColor(229, 219, 255)

    def get_selected_filter(self, state, name):
        if state == Qt.Checked:
            return name
        else:
            return ""

    def closeEvent(self, event):
        settings_manager = SettingsManager.instance()
        color = self.get_selected_color()
        settings_manager.set_background_color(color)
        filters = []
        filters.append(self.get_selected_filter(
            self.birthdays_checkbox.checkState(), "Urodziny"))
        filters.append(self.get_selected_filter(
            self.name_day_checkbox.checkState(), "Imieniny"))
        filters.append(self.get_selected_filter(
            self.holiday_checkbox.checkState(), "Święta"))
        filters.append(self.get_selected_filter(
            self.cultural_checkbox.checkState(), "Kulturalne"))
        filters.append(self.get_selected_filter(
            self.business_checkbox.checkState(), "Biznesowe"))
        filters.append(self.get_selected_filter(
            self.scientific_checkbox.checkState(), "Naukowe"))
        filters.append(self.get_selected_filter(
            self.other_checkbox.checkState(), "Inne"))
        settings_manager.set_filters(filters)
        event.accept()
