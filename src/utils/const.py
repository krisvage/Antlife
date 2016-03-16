""" Constants relevant for all modules. """

from collections import namedtuple

Status = namedtuple(
    'Status',
    ['OPEN', 'CLOSED', 'NEW']
)

SearchMode = namedtuple(
    'SearchMode',
    ['A_STAR', 'DFS', 'BFS']
)

Verbosity = namedtuple(
    'Verbosity',
    ['DEBUG', 'VERBOSE', 'SILENT', 'TEST']
)

NavTile = namedtuple(
    'NavTile',
    ['TILE', 'OBSTACLE', 'START', 'GOAL', 'PRINT_OBSTACLE']
)

Colors = namedtuple(
    'Colors',
    ['PINK', 'YELLOW', 'GREY', 'WHITE']
)

GraphColors = namedtuple(
    'GraphColors',
    ['RED', 'GREEN', 'BLUE', 'ORANGE', 'PINK', 'YELLOW', 'PURPLE',
     'BROWN', 'CYAN', 'DARK_BROWN', 'WHITE', 'BLACK', ]
)

Constants = namedtuple(
    'Constants',
    ['status', 'search_mode', 'verbosity', 'nav_tile', 'colors', 'graph_colors']
)

C = Constants(
    Status(1, 2, 3),
    SearchMode(1, 2, 3),
    Verbosity(1, 2, 3, 4),
    NavTile(1, 2, 3, 4, '#'),
    Colors(0, 1, 2, 3),
    GraphColors(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
)
