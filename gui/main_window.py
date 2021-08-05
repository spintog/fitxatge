from params import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.uic import loadUi
from sign_manager.sign_manager import SignManager
from database_manager.database_manager import DatabaseManager
from .system_tray import SystemTray
from .settings_window import SettingsWindow
from .about_window import AboutWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tray = SystemTray(self)
        self.tray.show()
        self.create_tray_actions()
        self.loadGui()

    def create_tray_actions(self):
        self.tray.add_action("Show window ", self.show)
        self.tray.add_separator()
        self.tray.add_action("Quit", self.quit_app)

    def loadGui(self):
        loadUi(gui_dir.joinpath("main.ui"), self)
        self.check_status()
        self.prefMenu.triggered.connect(SettingsWindow)
        self.aboutMenu.triggered.connect(AboutWindow)
        self.exitMenu.triggered.connect(self.quit_app)
    
    def check_status(self):
        # Obtain user settings from database
        self.database_manager = DatabaseManager(database_file)
        self.database_manager.create_connection()
        user_settings = self.database_manager.fetch_settings()
        self.database_manager.close_connection()
        if user_settings:
            self.server_url = user_settings[1]
            self.token = user_settings[2]
            config = {
                "token": self.token,
                "base_url": self.server_url
            }
        else:
            QMessageBox.critical(self, 'Error', "No user's settings found. Verify settings.", QMessageBox.Ok | QMessageBox.Cancel)
            SettingsWindow()
        
        # Check status server
        sign_manager = SignManager(config)
        if sign_manager.get_server_status():
            if sign_manager.get_status():
                self.statusLabel.setText("Treballant")
                self.statusLabel.setStyleSheet("background-color: Red")
                self.statusLabel.setStatusTip("En horari laboral")
                self.signButton.setText("Fitxar sortida")
                self.tray.set_tray_icon("inoffice")
            else:
                self.statusLabel.setText("Fora de feina")
                self.statusLabel.setStyleSheet("background-color: Green")
                self.statusLabel.setStatusTip("Fora d'horari laboral")
                self.signButton.setText("Fitxar entrada")
                self.tray.set_tray_icon("outoffice")


    def change_status(self):
        sign_status = self.sign.change_status()
        if sign_status:
            QMessageBox.information(self, 'Informació', 'Fitxatge realitzat correctament.', QMessageBox.Ok | QMessageBox.Ok)
            self.check_status()
        else:
            QMessageBox.critical(self, 'Error', "Error en el fitxatge: {}".format(sign_status), QMessageBox.Ok | QMessageBox.Ok)

    @pyqtSlot()
    def quit_app(self):
        QCoreApplication.instance().quit()
