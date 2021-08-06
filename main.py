from sqlite3.dbapi2 import Error
import sys
from params import database_file
from params import gui_dir
from params import img_dir
from database_manager.database_manager import DatabaseManager
from gui.main_window import MainWindow
from gui.settings_window import SettingsWindow
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication


def check_base_dirs(dir):
    ''' Function to check base directories'''
    if not dir.exists():
        QMessageBox.critical(
            None,
            'Error',
            '{} not found. Reinstall application'.format(dir.resolve()),
            QMessageBox.Ok | QMessageBox.Cancel)
        raise Exception


def check_database_status():
    '''Function to check database status'''
    database_manager = DatabaseManager(database_file)
    database_status = database_manager.check_database()

    if database_status == "NotFound":
        message_box = QMessageBox.critical(
            None,
            'Error',
            '{}. Initialise?'.format(database_status),
            QMessageBox.Ok | QMessageBox.Cancel)
        if message_box.real == 1024:
            try:
                database_manager.create_connection()
                database_manager.initialitze_database()
                database_manager.close_connection()
                check_database_status()
            except Error as error:
                raise error
        else:
            raise Exception
    elif database_status == "Empty":
        message_box = QMessageBox.critical(
            None,
            'Error',
            'Introduce settings', QMessageBox.Ok | QMessageBox.Cancel)
        if message_box.real == 1024:
            SettingsWindow()
        else:
            raise Exception


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Check if system suport system tray
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(
            None,
            'Error',
            'I couldn\'t detect any system tray on this system.')
        sys.exit(1)

    # Verify base directory are present on disk
    check_base_dirs(gui_dir)
    check_base_dirs(img_dir)

    # Verify database status
    check_database_status()

    QApplication.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
