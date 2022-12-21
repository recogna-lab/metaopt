from opytimark.markers.two_dimensional import *


def get_function(function):
    function_class = globals()[function]
    return function_class()