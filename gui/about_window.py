from params import *
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class AboutWindow(QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.loadUI()

    def loadUI(self):
        self.settingsWindow = loadUi(gui_dir.joinpath("about.ui"))
        self.settingsWindow.exec()