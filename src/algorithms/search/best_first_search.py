""" Implement the agenda loop and helper methods of A* """
import time
import heapq as q
from src.utils.const import C


class BestFirstSearch(object):
    """ Implement A*. Contains methods that raise NotImplementedError,
     so should be treated as an abstract base class.
    """

    def __init__(self, start, gui=None, retain=False):
        self.start = start
        self.gui = gui
        self.mode = C.search_mode.A_STAR if not gui else gui.mode
        self.delay = 50 if not gui else gui.delay  # milliseconds
        self.verbosity = C.verbosity.VERBOSE
        self.retain = retain
        self.gac = None

    def attach_and_eval(self, child, parent):
        """ Attach parent to child and find calculate the child costs """
        child.parent = parent
        child.g = parent.g + self.arc_cost(parent, child)
        child.h = child.heuristic_evaluation()
        child.f = child.g + child.h

    def propagate_path_improvements(self, parent):
        """ Propagate improvements down to the children """
        for child in parent.kids:
            if parent.g + self.arc_cost(parent, child) < child.g:
                child.parent = parent
                child.g = parent.g + self.arc_cost(parent, child)
                child.f = child.g + child.h
                self.propagate_path_improvements(child)

    def best_first_search(self):
        """ The agenda loop, runs until a solution is found and returned,
         or until we no longer find new successor nodes.
        """
        opened, generated, t_0 = [], {}, time.time()
        x, closed, closed_counter = None, None, None
        if self.retain:
            closed = []
        else:
            closed_counter = 0

        root = self.create_root_node()
        root.g, root.h = 0, root.heuristic_evaluation()
        root.f = root.g + root.h

        generated[root.sid] = root
        self.open_push(opened, root)

        while opened:
            x = self.open_pop(opened)

            self.node_closed(x, t_0, generated, opened, closed, closed_counter)

            if self.retain:
                closed.append(x)
            else:
                closed_counter += 1

            if x.is_solution():
                self.status_message(x, t_0, generated, closed, closed_counter)
                return x

            for s in x.generate_all_successors():
                if s.sid in generated:
                    s = generated[s.sid]

                x.add_child(s)

                if s.status is C.status.NEW:
                    self.attach_and_eval(s, x)

                    generated[s.sid] = s
                    self.open_push(opened, s)
                elif (x.g + self.arc_cost(x, s)) < s.g:
                    self.attach_and_eval(s, x)
                    if s.status is C.status.CLOSED:
                        self.propagate_path_improvements(s)

        self.status_message(x, t_0, generated, closed, closed_counter)

    def arc_cost(self, a, b):
        """ An estimate of the cost of moving from a to b """
        raise NotImplementedError(
            'Implement arc_cost() in BestFirstSearch subclass')

    def create_root_node(self):
        """ Return an instance of a SearchState subclass """
        raise NotImplementedError(
            'Implement create_root_node() in BestFirstSearch subclass')

    def open_push(self, opened, node):
        """ Push node onto opened according to mode, and set status """
        node.status = C.status.OPEN

        if self.mode is C.search_mode.A_STAR:
            q.heappush(opened, (node.f, node))
        elif self.mode is C.search_mode.DFS or self.mode is C.search_mode.BFS:
            opened.append(node)

    def open_pop(self, opened):
        """Pop node from opened according to mode """
        if self.mode is C.search_mode.A_STAR:
            return q.heappop(opened)[1]
        elif self.mode is C.search_mode.DFS:
            return opened.pop()
        elif self.mode is C.search_mode.BFS:
            return opened.pop(0)

    def node_closed(self, node, t_0, generated, opened, closed, closed_cnt):
        # pylint: disable=too-many-arguments
        """ Called when node is popped from opened, notifies GUI if needed """
        node.status = C.status.CLOSED

        if self.gui:
            if self.retain:
                self.gui.set_opened_closed(opened, closed)
            self.gui.paint(node)
            time.sleep(self.delay / 1000.0)

        if self.verbosity is not C.verbosity.DEBUG:
            return

        self.status_message(node, t_0, generated, closed, closed_cnt, False)

    def status_message(self, solution, t_0, generated, closed, cnt, paint=True):
        # pylint: disable=too-many-arguments
        """ Based on GUI and verbosity, shows the status of the search """
        if self.gui and paint:
            self.gui.paint(solution)
        else:
            if self.verbosity is C.verbosity.DEBUG:
                solution.print_level()

        t_1 = time.time()

        if self.retain:
            closed_length = len(closed)
        else:
            closed_length = cnt

        if self.gac:
            num_unsatisfied_constraints = len(
                [c for c in self.gac.constraints if not c.satisfied]
            )
            num_without_colors = len(
                [v for v in solution.domains.values() if len(v) != 1]
            )

            message = 'Nodes generated: {}, Nodes expanded: {}, '\
                      'Path length: {}\nUnsatisfied constraints: {}, '\
                      'Unassigned variables: {}, Time elapsed: {:.5f} sec'\
                .format(
                    len(generated), closed_length, solution.solution_length(),
                    num_unsatisfied_constraints, num_without_colors, t_1 - t_0
                )
        else:
            message = 'Nodes generated: {}, Nodes expanded: {}, '\
                      'Path length: {}, Time elapsed: {:.5f} sec'\
                .format(
                    len(generated), closed_length, solution.solution_length(),
                    t_1 - t_0
                )

        if self.verbosity in [C.verbosity.TEST, C.verbosity.SILENT]:
            return

        if self.gui:
            self.gui.status_message.emit(str(message))
        else:
            print(message + '\n')
