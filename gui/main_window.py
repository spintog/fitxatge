from params import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.loadGui()

    def loadGui(self):
        loadUi(gui_dir.joinpath("main.ui"), self)
