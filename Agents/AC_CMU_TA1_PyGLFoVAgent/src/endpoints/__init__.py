"""
A set of classes defining endpoints specific to the PyGLFoV agent.  The 
interface to endpoints follow that of pygl_fov:  Endpoint instances are 
callable objects that take a 2D pixel ID map as an argument.  As opposed to
pygl_fov endpoints, PyGLFoVAgent endpoints should *NOT* return any values.
"""

from .visualizer import MatplotVisualizer
from .block_summary import BlockSummaryMessageEndpoint
from .block_list import BlockLocationListMessageEndpoint

__all__ = ["MatplotVisualizer", 
           "BlockSummaryMessageEndpoint",
           "BlockLocationListMessageEndpoint"]

# The factories dictionary maps from a string representation of the class
# name of the endpoint to a correponding factory.
factories = {
	"MatplotVisualizer": MatplotVisualizer.Factory,
	"BlockSummaryMessageEndpoint": BlockSummaryMessageEndpoint.Factory,
	"BlockLocationListMessageEndpoint": BlockLocationListMessageEndpoint.Factory
}