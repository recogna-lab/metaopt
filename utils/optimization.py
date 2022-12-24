from opytimark.markers.two_dimensional import *
from opytimizer.optimizers.evolutionary import *
from opytimizer.optimizers.science import *
from opytimizer.optimizers.swarm import *


# Get optimizer class through its acronym 
def get_optimizer(optimizer):
    optimizer_class = globals()[optimizer]
    return optimizer_class()


# Get function class through its short name 
def get_function(function):
    function_class = globals()[function]
    return function_class()