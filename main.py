import sys
from params import *
from gui.main_window import MainWindow
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication

def check_base_dirs(dir):
    ''' Function to check base directories'''
    if not dir.exists():
        QMessageBox.critical(None, 'Error', "{} not found. Reinstall application".format(dir.resolve()), QMessageBox.Ok | QMessageBox.Ok)
        raise Exception
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Check if system suport system tray
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, QCoreApplication.translate("MainWindow", "Demerio"),
                             QCoreApplication.translate("MainWindow", "I couldn't detect any system tray on this system."))
        sys.exit(1)
    
    # Verify base directory are present on disk
    check_base_dirs(gui_dir)
    check_base_dirs(img_dir)
    
    QApplication.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
