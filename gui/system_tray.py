from os import setregid

from PyQt5.QtGui import QIcon
from params import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtWidgets import QWidget

class SystemTray(QWidget):

    def __init__(self, parent=None):
        super(SystemTray, self).__init__(parent)
        self.tray_icon_menu = QMenu(self)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(str(img_dir.joinpath("window_icon.png").resolve())))
        self.tray_icon.setContextMenu(self.tray_icon_menu)

    def add_action(self, name, triggered_action):
        action = QAction(QCoreApplication.translate("Exit", name), self, triggered = triggered_action)
        self.tray_icon_menu.addAction(action)

    def add_separator(self):
        self.tray_icon_menu.addSeparator()

    def show(self):
        super(SystemTray, self).show()
        self.tray_icon.show()

    def notify(self, title, message):
        self.tray_icon.showMessage(title, message, "Test")