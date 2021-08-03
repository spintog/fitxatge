from params import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QCoreApplication
from PyQt5.uic import loadUi
from .system_tray import SystemTray

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tray = SystemTray(self)
        self.tray.show()
        self.create_tray_actions()
        self.loadGui()

    def create_tray_actions(self):
        self.tray.add_action("Preference", self.show)
        self.tray.add_separator()
        self.tray.add_action("Quit", self.quit_app)

    def loadGui(self):
        loadUi(gui_dir.joinpath("main.ui"), self)

    @pyqtSlot()
    def quit_app(self):
        if self.daemon is not None:
            self.daemon.should_exit = True
            self.daemon.join()
        QCoreApplication.instance().quit()

