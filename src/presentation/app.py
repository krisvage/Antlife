""" Unified app for the entire course """
from PyQt4 import QtGui

from src.presentation.navigation.main_window import MainWindow as Navigation

class App(object):
    """ Loads a navigation window as default, and lets the user choose between
    all the different modules from the course """
    def __init__(self, qt_app):
        self.qt_app = qt_app
        self.main_window = Navigation()
        self.qt_app.setActiveWindow(self.main_window)

        self.add_switcher_menu()

    def loader(self, cls):
        self.main_window.close()
        self.main_window = cls()
        self.qt_app.setActiveWindow(self.main_window)

        self.add_switcher_menu()

    def navigation(self):
        """ Loads a Navigation instance into main window """
        self.loader(Navigation)

    def add_switcher_menu(self):
        """ Adds the following items to the menubar:
         Modules -> [ Navigation ]
        """
        navigation_action = QtGui.QAction('&Navigation', self.main_window)
        navigation_action.triggered.connect(self.navigation)

        menu = self.main_window.menuBar()
        module_menu = menu.addMenu('&Modules')
        module_menu.addAction(navigation_action)


def main():
    """ Creates Qt app and loads default level """
    import sys
    qt_app = QtGui.QApplication(sys.argv)
    _ = App(qt_app)
    sys.exit(qt_app.exec_())

if __name__ == '__main__':
    main()
