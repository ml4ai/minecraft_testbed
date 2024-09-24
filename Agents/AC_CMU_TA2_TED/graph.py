#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import numpy as np

with open('results/visited-ac.json', 'rt') as in_file:
    visited_ac = json.load(in_file)

with open('results/visited-base.json', 'rt') as in_file:
    visited_base = json.load(in_file)

print(f'{len(visited_ac)} vs. {len(visited_base)}')

minx_ac = min([x[0] for x in visited_ac])
maxx_ac = max([x[0] for x in visited_ac])
miny_ac = min([x[1] for x in visited_ac])
maxy_ac = max([x[1] for x in visited_ac])
print(f'ac bounds: {minx_ac}, {maxx_ac} - {miny_ac}, {maxy_ac}')

visited_ac = [(x+1, y+1) for x, y in visited_ac]

minx_base = min([x[0] for x in visited_base])
maxx_base = max([x[0] for x in visited_base])
miny_base = min([x[1] for x in visited_base])
maxy_base = max([x[1] for x in visited_base])
print(f'base bounds: {minx_base}, {maxx_base} - {miny_base}, {maxy_base}')

width = max(maxx_ac - minx_ac, maxx_base - minx_base) + 1
height = max(maxy_ac - miny_ac, maxy_base - miny_base) + 1

grid = np.zeros(shape=(height, width, 3), dtype=float)

for pos in visited_base:
    x = pos[0] - minx_base
    y = pos[1] - miny_base
    grid[y][x][0] = 1

for pos in visited_ac:
    x = pos[0] - minx_ac
    y = pos[1] - miny_ac
    grid[y][x][1] = 1

plt.figure(figsize=(12, 12))
plt.imshow(grid, interpolation='none')
plt.savefig('results/plot.png')
