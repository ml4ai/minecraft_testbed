
import pygl_fov
from pygl_fov.endpoints import SemanticMapVisualizer, BlockListSummary
from pygl_fov.vertex_store import StaticVboStore


# Setup
perspective = pygl_fov.Perspective(position=(-2139.0, 52.0, 176.0),
	                               orientation=(0.0, 0.0, 0.0),
	                               window_size=(852, 480))

feeder = pygl_fov.BlockFeeder.loadFromJson("data/map_blocks.json")
vertex_store = StaticVboStore(feeder)

fov = pygl_fov.FOV(perspective, vertex_store, False)

summary = BlockListSummary(feeder)


# Usage
# GET PLAYER POSITION & ORIENTATION FROM MALMO / ASIST
angle=90
perspective.set_orientation=(0.0, angle, 0.0)

pixelmap = fov.calculatePixelToBlockIdMap()	# NOTE: Can probably have summary calculate this.

for block in summary(pixelmap):
	print(f'Block Location: {block["block"].location}\tBlock Type: {block["block"].block_type}\tNum Pixels: {block["pixel_count"]}')

# Repeat
