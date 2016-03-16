""" Represent a node in A* search """
from src.utils.const import C


class SearchState(object):
    """ A search state contains a representation of the state, an unique
     id, the cost estimate and calculation, as well as pointer to the best
     parent and all kids. The status is set so that we save some O(n) lookups
     in the agenda loop
    """

    def __init__(self, state):
        self.state = state  # An object describing a state of the search process
        self.sid = self.create_state_identifier()

        self.g = None  # Cost of getting to this node
        self.h = None  # Estimated cost to goal
        self.f = None  # Estimated total cost of a solution path going
        #  through this node; f = g + h

        self.parent = None  # Pointer to best parent node
        self.kids = []   # list of all successor nodes, whether or not this
        #  node is currently their best parent.

        self.status = C.status.NEW  # OPEN / CLOSED / NEW

    def heuristic_evaluation(self):
        """ Returns an estimate of distance to goal """
        raise NotImplementedError(
            'Implement compute_h() in SearchState subclass')

    def create_state_identifier(self):
        """ Creates a unique id based on state """
        raise NotImplementedError(
            'Implement create_state_identifier() in SearchState subclass')

    def generate_all_successors(self):
        """ Generate a list of successors """
        raise NotImplementedError(
            'Implement generate_all_successors() in SearchState subclass')

    def is_solution(self):
        """ Return whether the current state is a valid solution """
        raise NotImplementedError(
            'Implement is_solution() in SearchState subclass')

    def solution_length(self):
        """ Return a length of the search path of the current state """
        raise NotImplementedError(
            'Implement solution_length() in SearchState subclass')

    def add_child(self, child):
        """ Add a child to this node """
        self.kids.append(child)

    def __lt__(self, other):
        return self.f < other.f
