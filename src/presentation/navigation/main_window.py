""" A GUI application for showing A* runs """
from PyQt4 import QtGui

import res.imgs
from src.utils.const import C
from src.utils.func import make_function
from src.presentation.navigation.navigation_gui import NavigationGUI


class MainWindow(QtGui.QMainWindow):
    """ The GUI window which contains the Widgets and buttons """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.nav_gui = NavigationGUI(self)

        self.init_ui()

    def init_ui(self):
        """ Initializes the UI, delegates to init_menubar and init_toolbar """
        self.setCentralWidget(self.nav_gui)

        self.init_menubar()
        self.init_toolbar()

        status_bar_label = QtGui.QLabel()
        status_bar_label.setWordWrap(True)
        status_bar_label.setFixedWidth(600)

        self.statusBar().addWidget(status_bar_label)
        self.nav_gui.status_message[str].connect(status_bar_label.setText)

        self.show()
        self.raise_()

    def init_menubar(self):
        # pylint: disable=too-many-locals
        """ Initializes a menubar with the following items:
         File -> [ Load, Kill, Exit ]
         Mode -> [ A*, DFS, BFS ]
        """
        load_action = QtGui.QAction('&Load map', self)
        load_action.setShortcut('Ctrl+L')
        load_action.triggered.connect(self.nav_gui.set_map)

        kill_action = QtGui.QAction('&Kill search', self)
        kill_action.setShortcut('Ctrl+K')
        kill_action.triggered.connect(self.nav_gui.thread.end_search)

        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)

        a_star_action = QtGui.QAction('&A* Mode', self)
        a_star_action.setShortcut('Ctrl+1')
        a_star_action.triggered.connect(
            lambda: (self.nav_gui.set_mode(C.search_mode.A_STAR) and
                     self.mode_changed(C.search_mode.A_STAR))
        )

        dfs_action = QtGui.QAction('&DFS Mode', self)
        dfs_action.setShortcut('Ctrl+2')
        dfs_action.triggered.connect(
            lambda: (self.nav_gui.set_mode(C.search_mode.DFS) and
                     self.mode_changed(C.search_mode.DFS))
        )

        bfs_action = QtGui.QAction('&BFS Mode', self)
        bfs_action.setShortcut('Ctrl+3')
        bfs_action.triggered.connect(
            lambda: (self.nav_gui.set_mode(C.search_mode.BFS) and
                     self.mode_changed(C.search_mode.BFS))
        )

        diagonal_on = QtGui.QAction('&On', self)
        diagonal_on.triggered.connect(
            lambda: (self.nav_gui.set_diagonal(True))
        )

        diagonal_off = QtGui.QAction('&Off', self)
        diagonal_off.triggered.connect(
            lambda: (self.nav_gui.set_diagonal(False))
        )

        euclidean_option = QtGui.QAction('&Euclidean distance', self)
        euclidean_option.triggered.connect(
            lambda: (self.nav_gui.set_heuristics_type('euclidean'))
        )

        manhattan_option = QtGui.QAction('&Manhattan distance', self)
        manhattan_option.triggered.connect(
            lambda: (self.nav_gui.set_heuristics_type('manhattan'))
        )

        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        file_menu.addAction(load_action)
        file_menu.addAction(kill_action)
        file_menu.addAction(exit_action)

        mode_menu = menu.addMenu('&Mode')
        mode_menu.addAction(a_star_action)
        mode_menu.addAction(dfs_action)
        mode_menu.addAction(bfs_action)

        diagonal_menu = menu.addMenu('&Diagonal')
        diagonal_menu.addAction(diagonal_on)
        diagonal_menu.addAction(diagonal_off)

        heuristics_menu = menu.addMenu('&Heuristics')
        heuristics_menu.addAction(euclidean_option)
        heuristics_menu.addAction(manhattan_option)

    def init_toolbar(self):
        """ Initializes a toolbar, with a run button and delay controls """
        play_icon = QtGui.QIcon(list(res.imgs.__path__).pop(0) + '/play.png')
        run_action = QtGui.QAction(play_icon, 'Run search', self)
        run_action.setShortcut('Ctrl+R')
        run_action.triggered.connect(self.nav_gui.start_search)

        toolbar = self.addToolBar('Run')
        toolbar.addAction(run_action)

        delays = [0, 50, 150, 500, 1000]
        for delay in delays:
            delay_action = QtGui.QAction('&Delay: ' + str(delay) + ' ms', self)
            expr = 'self.nav_gui.set_delay({})'.format(delay)
            delay_action.triggered.connect(make_function([], expr, locals()))
            toolbar.addAction(delay_action)

    def mode_changed(self, mode):
        """ Writes to status bar when mode is changed """
        mode_s = {
            C.search_mode.A_STAR: 'A*',
            C.search_mode.BFS: 'BFS',
            C.search_mode.DFS: 'DFS'
        }[mode]

        self.nav_gui.status_message.emit('Mode: ' + mode_s)


def main():
    """ Creates Qt app and loads default level """
    import sys
    app = QtGui.QApplication(sys.argv)

    _ = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
