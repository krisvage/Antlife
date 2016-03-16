# from src.utils.debug import debug; debug(locals())

import code


debug = lambda l: code.interact(local=l)
