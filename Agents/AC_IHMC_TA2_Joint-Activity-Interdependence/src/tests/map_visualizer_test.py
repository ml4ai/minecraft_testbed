"""
Manual visualizer test environment

author: Micael Vignati
email: mvignati@ihmc.org
"""

__author__ = 'mvignati'

from .static_blockage_list import blockages, victims
from ..models.local_client import LocalClient
from ..views.map_view import MapView

local_client = LocalClient()
visualizer = MapView(local_client)
# load map after visualizer is initialized
local_client.map.load_map_data('Saturn_2.4_3D-fov_map')
local_client.map.update_map(blockages)
local_client.map.update_map(victims)
visualizer.start_rendering_loop()
