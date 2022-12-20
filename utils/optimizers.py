from opytimizer.optimizers.boolean import *
from opytimizer.optimizers.evolutionary import *
from opytimizer.optimizers.misc import *
from opytimizer.optimizers.population import *
from opytimizer.optimizers.science import *
from opytimizer.optimizers.social import *
from opytimizer.optimizers.swarm import *


def get_optimizer(optimizer):
    optimizer_class = globals()[optimizer]
    return optimizer_class()