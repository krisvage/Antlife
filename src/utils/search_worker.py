""" Worker thread for performing search outside of GUI thread """
from PyQt4.QtCore import QThread


class SearchWorker(QThread):
    """ Inherit QThread for easy threading """

    def __init__(self, gui, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.gui, self._search = gui, None

    def search(self, search):
        """ Sets up gui and search, and proceeds to start itself """
        self._search = search

        self.start()

    def run(self):
        """ Called when thread is started, perform search and set solution
         create a NonogramState node that can be set in the GUI
        """
        solution = self._search.best_first_search()

        if solution:
            self.gui.set_solution(solution)

    def end_search(self):
        """ Terminates thread """
        self.setTerminationEnabled(True)
        self.terminate()
        self.gui.status_message.emit('Search killed')

    def __del__(self):
        self.exiting = True
        self.wait()
