""" A Widget for drawing Navigation states """
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

import os
import res.maps
from src.utils.const import C
from src.utils.search_worker import SearchWorker
from src.specializations.navigation.map import Map
from src.specializations.navigation.navigation_bfs import NavigationBfs
from src.specializations.navigation.navigation_state import NavigationState


class NavigationGUI(QtGui.QFrame):
    # pylint: disable=too-many-instance-attributes
    """ Implement QFrame, which is a subclass of QWidget """
    status_message = pyqtSignal(str)

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.dx = self.dy = 0
        self.widget_width_px = self.widget_height_px = 600

        self.delay = 50
        self.diagonal = False
        self.mode = C.search_mode.A_STAR
        self.heuristics_type = 'euclidean'

        self.node = None
        self.opened = None
        self.closed = None
        self.set_map(True)
        self.thread = SearchWorker(self)
        self.init_ui()

    def init_ui(self):
        """ Initialize the UI """
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        minimum_size = QtCore.QSize(self.widget_width_px, self.widget_height_px)
        self.setMinimumSize(minimum_size)
        self.parent().adjustSize()

    def level_loaded(self, map_):
        """ Called whenever a level is loaded, adjust Widget size """
        self.node = NavigationState(map_)
        self.opened, self.closed = None, None
        self.compute_tile_size()

    def compute_tile_size(self):
        """ Computes tile size based on widget size and map """
        self.dx = self.widget_width_px / float(self.node.state.x_dim())
        self.dy = self.widget_height_px / float(self.node.state.y_dim())

    def start_search(self):
        """ Start the search in the worker thread """
        navigation = NavigationBfs(self.node.state, self)

        self.status_message.emit(str('Search started'))
        self.thread.search(navigation)

    def set_solution(self, solution):
        """ Receives a solution from search and sets the node """
        self.node = NavigationState(
            self.node.state,
            solution.visited,
            solution.current_pos
        )

    def set_opened_closed(self, opened, closed):
        """ Sets the opened and closed lists of states """
        self.opened = opened
        self.closed = closed

    def paint(self, node):
        """ Receives a node and tells Qt to update the graphics """
        self.node = node

        self.update()

    def paintEvent(self, _):  # pylint: disable=invalid-name
        """ Called by the Qt event loop when the widget should be updated """
        if self.node is None:
            return

        painter = QtGui.QPainter(self)
        self.paint_map(painter)

    def resizeEvent(self, e):  # pylint: disable=invalid-name
        """ Handles widget resize and scales Navigation """
        self.widget_width_px = e.size().width()
        self.widget_height_px = e.size().height()
        self.compute_tile_size()

    def is_visited(self, x, y):
        """ Checks whether (x,y) is visited in the current state """
        y_dim = self.node.state.y_dim()
        pos = [x, y_dim - y - 1]
        return pos in self.node.visited

    def is_on_frontier(self, x, y):
        """ Checks whether (x,y) is in the opened list """
        if not self.opened:
            return False

        y_dim = self.node.state.y_dim()

        for node in self.opened:
            if isinstance(node, tuple):
                node = node[1]  # Heapq for astar, normal list for BFS/DFS

            if [x, y_dim - y - 1] == node.visited[-1]:
                return True

        return False

    def is_closed(self, x, y):
        """ Checks whether (x,y) is in the closed list """
        if not self.closed:
            return False

        y_dim = self.node.state.y_dim()

        for node in self.closed:
            if [x, y_dim - y - 1] == node.visited[-1]:
                return True

        return False

    def get_color(self, x, y, visited=False, frontier=False, closed=False):
        # pylint: disable=too-many-arguments
        """ Return a QColor based on the tile and whether it is visited """

        if visited:
            color = {
                C.nav_tile.TILE:  QtGui.QColor(80, 80, 80),
                C.nav_tile.START: QtGui.QColor(153, 204, 255),
                C.nav_tile.GOAL:  QtGui.QColor(0, 255, 0)
            }[self.node.state.grid[y][x]]
        elif frontier:
            color = QtGui.QColor(255, 255, 80)
        elif closed:
            color = QtGui.QColor(210, 210, 210)
        else:
            color = {
                C.nav_tile.TILE:     QtGui.QColor(255, 255, 255),
                C.nav_tile.OBSTACLE: QtGui.QColor(255, 0, 0),
                C.nav_tile.START:    QtGui.QColor(0, 0, 255),
                C.nav_tile.GOAL:     QtGui.QColor(51, 102, 0)
            }[self.node.state.grid[y][x]]

        return color

    def draw(self, x, y, painter):
        """ Draws rectangles, either with a black border or without a border.
         If the tile is visited we draw a smaller rectangle on top.
        """
        color = self.get_color(x, y)
        dx, dy = self.dx, self.dy

        if self.node.state.grid[y][x] is C.nav_tile.OBSTACLE:
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))
        else:
            painter.setPen(QtGui.QPen(color, 1))
        painter.setBrush(color)
        painter.drawRect((x * dx), (y * dy), dx - 1, dy - 1)

        is_visited = self.is_visited(x, y)
        is_on_frontier = self.is_on_frontier(x, y)
        is_closed = self.is_closed(x, y)
        if is_visited or is_on_frontier or is_closed:
            color = self.get_color(x, y, is_visited, is_on_frontier, is_closed)
            painter.setPen(QtGui.QPen(color, 1))
            painter.setBrush(color)
            painter.drawRect((x * dx) + 4, (y * dy) + 4, dx - 9, dy - 9)

    def paint_map(self, painter):
        """ Called by the paintEvent, we iterate over the map and draw tiles """
        for y in range(self.node.state.y_dim()):
            for x in range(self.node.state.x_dim()):
                self.draw(x, y, painter)

    def set_map(self, default=False):
        """ Load level with a QFileDialog """
        folder = list(res.maps.__path__).pop()

        if default:
            path = folder + '/ex5.txt'
        else:
            path = QtGui.QFileDialog.getOpenFileName(
                self.window(), "Open Map File", folder, "Text files (*.txt)"
            )
            if not path:
                return

        map_file = open(path, 'r')
        contents = [line.strip() for line in map_file.read().splitlines()]

        self.level_loaded(Map(contents))

        filename = path.split('/')[-1]
        self.parent().setWindowTitle(
            'Module 1 - Navigation - {}'.format(filename)
        )
        self.status_message.emit(str('Loaded: {}'.format(filename)))
        self.update()

    def set_mode(self, mode):
        """ Chainable method for use in lambdas, change mode """
        self.mode = mode
        return True

    def set_delay(self, delay):
        """ Change delay """
        self.delay = delay
        self.status_message.emit('Delay: ' + str(delay))

    def set_diagonal(self, is_diagonal):
        """ Set diagonal mode """
        self.diagonal = is_diagonal
        self.status_message.emit('Diagonal mode: ' + str(is_diagonal))

    def set_heuristics_type(self, heuristics_type):
        """ Set heuristics """
        self.heuristics_type = heuristics_type
        message = 'Heuristics: ' + str(heuristics_type) + ' distance'
        self.status_message.emit(message)
