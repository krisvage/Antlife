""" Specialization of SearchState """
from src.algorithms.search.search_state import SearchState
from src.utils.const import C
from src.utils.id_generator import ID_GENERATOR
from copy import deepcopy


class NavigationState(SearchState):
    """ A navigation, containing the state of the map as a NavigationGrid """

    def __init__(self, navigation, visited=None, current_pos=None,
                 diagonal=False, heuristics_type=None):
        # pylint: disable=too-many-arguments
        self.visited = visited or [navigation.agent_positions.pop(0)] # TODO: Something here
        self.current_pos = current_pos or navigation.agent_positions.pop(0)
        self.diagonal = diagonal
        self.heuristics_type = heuristics_type
        SearchState.__init__(self, navigation)

    def create_state_identifier(self):
        current_pos_str = ','.join([str(el) for el in self.current_pos])
        return ID_GENERATOR.get_id(current_pos_str)

    def heuristic_evaluation(self):
        """ Returns the euclidean distance from the goal to current tile.
         Euclidean distance gave better results on some boards vs. manhattan
        """
        if self.heuristics_type == 'euclidean':
            return self.euclidean_distance(self.state.goal, self.current_pos)
        elif self.heuristics_type == 'manhattan':
            return self.manhattan_distance(self.state.goal, self.current_pos)

        return self.euclidean_distance(self.state.goal, self.current_pos)

    @staticmethod
    def euclidean_distance(a, b):
        """ sqrt(x^2 + y^2) """
        x, y = (b[0] - a[0]) ** 2, (b[1] - a[1]) ** 2
        return (x + y) ** 0.5

    @staticmethod
    def manhattan_distance(a, b):
        """ x + y """
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def is_solution(self):
        return self.h == 0.0

    def solution_length(self):
        return len(self.visited)

    def generate_all_successors(self):
        if self.diagonal:
            viable_movements = [[-1, -1], [1, 1], [1, -1], [-1, 1],
                                [-1, 0], [1, 0], [0, -1], [0, 1]]
        else:
            viable_movements = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        successors = []

        for move in viable_movements:
            pos = self.current_pos
            x_dim = self.state.x_dim()
            y_dim = self.state.y_dim()

            next_pos = [pos[0] - move[0], pos[1] - move[1]]
            x = next_pos[0]
            y = y_dim - next_pos[1] - 1

            if x < 0 or x > (x_dim - 1):
                continue

            if y < 0 or y > (y_dim - 1):
                continue

            if self.state.grid[y][x] == C.nav_tile.OBSTACLE:
                continue

            if next_pos in self.visited:
                continue

            visited = deepcopy(self.visited) + [next_pos]

            successor = NavigationState(
                self.state, visited, next_pos, self.diagonal,
                self.heuristics_type
            )

            successors.append(successor)

        return successors

    def print_level(self):
        """ Prints map as text, with visited tiles marked """
        x_dim = self.state.map.x_dim()
        y_dim = self.state.map.y_dim()

        output = [[0] * x_dim for _ in range(y_dim)]

        for pos in self.state.visited_copy():
            output[y_dim - pos[1] - 1][pos[0]] = 1

        for i, row in enumerate(self.state.map.grid):
            for j, element in enumerate(row):
                if element is C.nav_tile.OBSTACLE:
                    output[i][j] = C.nav_tile.PRINT_OBSTACLE

        print('\n'.join([' '.join([str(el) for el in row]) for row in output]))
