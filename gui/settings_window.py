from params import database_file
from params import gui_dir
from database_manager.database_manager import DatabaseManager
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTime
from PyQt5.uic import loadUi


class SettingsWindow(QWidget):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.database_manager = DatabaseManager(database_file)
        self.database_manager.create_connection()
        user_settings = self.database_manager.fetch_settings()

        if user_settings:
            self.user_id = user_settings[0]
            self.server_url = user_settings[1]
            self.user_token = user_settings[2]
            self.in_morning = user_settings[3]
            self.out_morning = user_settings[4]
            self.in_afternoon = user_settings[5]
            self.out_afternoon = user_settings[6]
        else:
            self.server_url = None
            self.user_token = None
            self.in_morning = None
            self.out_morning = None
            self.in_afternoon = None
            self.out_afternoon = None
            self.user_id = None

        self.loadUI()

    def loadUI(self):
        self.settingsWindow = loadUi(gui_dir.joinpath("settings.ui"))
        self.settingsWindow.urlInput.setText(self.server_url)
        self.settingsWindow.tokenInput.setText(self.user_token)
        self.settingsWindow.inMorningTime.setTime(
            QTime.fromMSecsSinceStartOfDay(self.in_morning)
        )
        self.settingsWindow.outMorningTime.setTime(
            QTime.fromMSecsSinceStartOfDay(self.out_morning)
        )
        self.settingsWindow.inAfternoonTime.setTime(
            QTime.fromMSecsSinceStartOfDay(self.in_afternoon)
        )
        self.settingsWindow.outAfternoonTime.setTime(
            QTime.fromMSecsSinceStartOfDay(self.out_afternoon)
        )
        self.settingsWindow.buttonBox.accepted.connect(self.save_settings)
        self.settingsWindow.exec()

    def save_settings(self):
        settings = {
            "server_url": self.settingsWindow.urlInput.text(),
            "user_token": self.settingsWindow.tokenInput.text(),
            "user_id": self.user_id,
            "in_morning": self.settingsWindow.inMorningTime.time()
                                             .msecsSinceStartOfDay(),
            "out_morning": self.settingsWindow.outMorningTime.time()
                                              .msecsSinceStartOfDay(),
            "in_afternoon": self.settingsWindow.inAfternoonTime.time()
                                               .msecsSinceStartOfDay(),
            "out_afternoon": self.settingsWindow.outAfternoonTime.time()
                                                .msecsSinceStartOfDay(),
        }

        update_result = self.database_manager.save_settings(settings)
        self.database_manager.close_connection()
        if update_result is True:
            QMessageBox.information(
                self,
                'Save Settings',
                'Settings saved correctly',
                QMessageBox.Ok | QMessageBox.Cancel)
        else:
            QMessageBox.critical(
                self,
                'Error',
                'Error al guardar els canvis: {}'.format(update_result),
                QMessageBox.Ok | QMessageBox.Cancel)
