#!/usr/bin/env python3

"""
IHMC map visualizer

author: Micael Vignati
email: mvignati@ihmc.org
"""

__author__ = 'mvignati'

import math

import numpy as np
import pygame as pg
import pygame.sprite

TILE_SIZE = 7
PLAYER_SIZE = 7
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

MAP_UPDATE = pygame.event.custom_type()


class MapView:

    def __init__(self, model):
        self.__render_layer = 2
        self.__model = model

        self.__model.map.on_map_update = self.__on_map_update
        self.__walls = pygame.sprite.Group()

        self.__window = None
        self.__init_window()

        self.__player_rect = pg.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.__visible_rect = pg.Rect(0, 0, TILE_SIZE, TILE_SIZE)

        self.__event_handlers = {
            pg.MOUSEMOTION: self.__handle_mouse_motion,
            pg.KEYDOWN: self.__handle_key_down,
        }

    def __on_map_update(self):
        width, height, _ = self.__model.map.dimensions * TILE_SIZE
        pg.event.post(pg.event.Event(MAP_UPDATE, {'dimensions': [width, height]}))

    def __init_window(self):
        self.__window = pg.display.set_mode((480, 320))
        pg.display.set_caption('ihmc map-visualizer')

    def __init_sprites(self):
        layer = self.__model.map.blocks[:, :, self.__render_layer]

        victim = pygame.Surface([TILE_SIZE, TILE_SIZE])
        victim.fill((255, 255, 0))
        rubble = pygame.Surface([TILE_SIZE, TILE_SIZE])
        rubble.fill((128, 128, 128))
        wall = pygame.Surface([TILE_SIZE, TILE_SIZE])
        wall.fill((255, 255, 255))

        block_mapping = {
            1: wall,
            2: victim,
            3: victim,
            4: victim,
            5: rubble,
        }

        self.__walls.empty()
        rows, cols = np.nonzero(layer)
        for i in range(len(rows)):
            x = rows[i]
            y = cols[i]
            block_type = layer[x, y]
            image = block_mapping[block_type]
            b = Block(image, (255, 255, 255), TILE_SIZE, TILE_SIZE, x * TILE_SIZE, y * TILE_SIZE)
            self.__walls.add(b)

    def __handle_user_event(self, event):
        if event.type not in self.__event_handlers:
            return
        self.__event_handlers[event.type](event)

    def __handle_mouse_motion(self, event):
        x, y = event.pos
        x_cell = math.floor(x / TILE_SIZE)
        y_cell = math.floor(y / TILE_SIZE)
        # x_cell = (x / TILE_SIZE)
        # y_cell = (y / TILE_SIZE)
        self.__model.handle_mouse_motion(x_cell, y_cell)

    def __handle_key_down(self, event):
        if event.key == 61:  # '+' increases layer
            self.__render_layer += 1
        elif event.key == 45:  # '-' decreases layer
            self.__render_layer -= 1
        elif event.key == pygame.K_LEFT:
            self.__model.handle_turn(1)
        elif event.key == pygame.K_RIGHT:
            self.__model.handle_turn(-1)

    def start_rendering_loop(self):
        clock = pg.time.Clock()
        run = True

        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__model.stop()
                    run = False
                if event.type == MAP_UPDATE:
                    self.__window = pg.display.set_mode(event.dimensions)
                    self.__init_sprites()

                self.__handle_user_event(event)
            self.render()
            pg.display.update()
            clock.tick(60)

        pg.quit()

    def render(self):
        self.__window.fill(BLACK)

        self.render_map()
        self.render_players()

    def render_map(self):
        self.__walls.draw(self.__window)
        return

    def render_players(self):
        players = self.__model.players.values()
        for player in players:
            self.__render_fov(player)

        for player in players:
            self.__player_rect.x = player.x * TILE_SIZE
            self.__player_rect.y = player.y * TILE_SIZE
            pg.draw.rect(self.__window, player.color, self.__player_rect)

        for player in players:
            player_location = (player.location + 0.5) * TILE_SIZE
            for x, y, t, id in player.points_of_interest.values():
                end_x = (x + .5) * TILE_SIZE
                end_y = (y + .5) * TILE_SIZE
                pg.draw.line(self.__window, np.array((255, 128, 255)), player_location, (end_x, end_y))

    def __render_fov(self, player):
        light = player.color * 0.5
        for idx in range(player.fov_length):
            if not player.fov_mask[idx]:
                continue
            block = player.fov[idx]
            self.__visible_rect.x = block[0] * TILE_SIZE
            self.__visible_rect.y = block[1] * TILE_SIZE
            pg.draw.rect(self.__window, light, self.__visible_rect)
        # arcs = np.array(player.arcs)
        # for i in range(0, len(arcs), 2):
        #     left = arcs[i]
        #     right = arcs[i + 1]
        #     player_location = (player.location + 0.5) * TILE_SIZE
        #     left_end = player_location + left * TILE_SIZE  # player.fov_radius # * TILE_SIZE
        #     right_end = player_location + right * TILE_SIZE  # player.fov_radius # * TILE_SIZE
        #     pg.draw.line(self.__window, np.array((0, 128, 255)), player_location, left_end)
        #     pg.draw.line(self.__window, (255, 128, 128), player_location, right_end)


class Block(pygame.sprite.Sprite):
    def __init__(self, surface, color, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
