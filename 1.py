import pygame
import os
import glob

DISPLAY_SIZE = (2000, 1000)


class ResourceManager:

    def __init__(self):
        self._resources = dict()
        self._map = dict()

    def load_resources(self):
        for path in glob.glob('data/*.jpg'):
            name = path.split('\\')[-1].split('.')[0]
            self._resources[name] = pygame.image.load(path).convert()

        for path in glob.glob('data/*.txt'):
            name = path.split('\\')[-1]
            with open(name, 'r') as mapFile:
                self._map = [line.strip() for line in mapFile]

    def get_resource(self, name):
        return self._resources[name]


class Tile(pygame.sprite.Sprite):

    def __init__(self, tile_type, pos_x, pos_y, resource_manager):
        super().__init__(self.tiles_group, self.all_sprites)

    def draw(self, surf):
        pass

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()


class Board:

    def __init__(self, width, height, x=10, y=10, cell_size=30):
        self._width = width
        self._height = height
        self._x = x
        self._y = y
        self._board = [[Tile() for i in range(height)] for _ in range(width)]
        self._cell_size = cell_size

    def get_cell(self, mouse_pos):
        mp = (mouse_pos[0] - self._x, mouse_pos[1] - self._y)
        cell_pos = (mp[0] // self._cell_size, mp[1] // self._cell_size)
        if not (cell_pos[0] < 0 or cell_pos[0] >= self._width or
                cell_pos[1] < 0 or cell_pos[1] >= self._height):
                return cell_pos
        return None

    def on_click(self, cell):
        self._board[cell[0]][cell[1]] = 1 - self._board[cell[0]][cell[1]]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def draw(self, surf):
        for i in range(self._width):
            for j in range(self._height):
                pygame.draw.rect(surf, pygame.Color('white'), (self._x + i * self._cell_size,
                                                               self._y + j * self._cell_size,
                                                               self._cell_size, self._cell_size),
                                1 - self._board[i][j])


pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)

board = Board(40, 40, cell_size=30)

tile_width = tile_height = 50




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)

    screen.fill((0, 0, 0))
    board.draw(screen)
    pygame.display.flip()

pygame.quit()