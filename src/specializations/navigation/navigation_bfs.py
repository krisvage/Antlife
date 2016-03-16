""" Navigation specialization of A* """
from src.algorithms.search.best_first_search import BestFirstSearch
from src.specializations.navigation.navigation_state import NavigationState
from src.specializations.navigation.map import Map


class NavigationBfs(BestFirstSearch):
    """ Map navigation version of A* """

    def __init__(self, start, gui=None):
        self.diagonal = False if not gui else gui.diagonal
        self.heuristics_type = 'euclidean' if not gui else gui.heuristics_type
        BestFirstSearch.__init__(self, start, gui, True)

    def create_root_node(self):
        return NavigationState(
            self.start, None, None, self.diagonal, self.heuristics_type
        )

    def arc_cost(self, a, b):
        if self.diagonal:
            return 1.1
        if self.heuristics_type == 'manhattan':
            return 0.9
        else:
            return 0.5


def main():
    """ Text-based test of Navigation """
    import res.maps
    path = res.maps.__path__[0] + '/ex0.txt'
    map_ = Map(open(path, 'r').read().splitlines())
    solution = NavigationBfs(map_).best_first_search()

    solution.print_level()
    if not solution:
        print('Failed')

if __name__ == '__main__':
    main()
