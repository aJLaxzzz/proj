import pygame
import os
import glob

DISPLAY_SIZE = (900, 1000)

TILE_SIZE = 64


class ResourceManager:

    def __init__(self):
        self._resources = dict()
        self._map = dict()

    def load_resources(self):
        for path in glob.glob('data/*.jpg'):
            name = path.split('\\')[-1].split('.')[0]
            self._resources[name] = pygame.transform.scale(pygame.image.load(path).convert(), (TILE_SIZE, TILE_SIZE))

        for path in glob.glob('data/*.txt'):
            name = path.split('\\')[-1]
            with open(path, 'r') as mapFile:
                self._map = [line.strip() for line in mapFile]

    def get_resource(self, name):
        return self._resources[name]

    def get_map(self):
        return self._map


class Tile:

    def __init__(self, tile_type, pos_x, pos_y, resource_manager):
        self.sprite = pygame.sprite.Sprite()
        self.type = tile_type
        self.sprite.image = resource_manager.get_resource(tile_type)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect = self.sprite.rect.move(pos_x, pos_y)

    def get_sprite(self):
        return self.sprite


class GameWorld:

    def __init__(self, resourse_manager, x=50, y=50):
        map = resourse_manager.get_map()
        self._width = len(map[0])
        self._height = len(map)
        self._x = x
        self._y = y
        self._board = [[None for i in range(self._width)] for _ in range(self._height)]
        self._tile_group = pygame.sprite.Group()
        map = resourse_manager.get_map()
        self._width = len(map[0])
        self._height = len(map)
        for x in range(self._height):
            for y in range(self._width):
                if map[x][y] == '.':
                    self._board[x][y] = Tile('sand', x * TILE_SIZE, y * TILE_SIZE, resourse_manager)
                elif map[x][y] == '#':
                    self._board[x][y] = Tile('tree', x * TILE_SIZE, y * TILE_SIZE, resourse_manager)
                elif map[x][y] == '&':
                    self._board[x][y] = Tile('grass', x * TILE_SIZE, y * TILE_SIZE, resourse_manager)
                elif map[x][y] == '%':
                    self._board[x][y] = Tile('tron', x * TILE_SIZE, y * TILE_SIZE, resourse_manager)
                elif map[x][y] == '/':
                    self._board[x][y] = Tile('tower1', x * TILE_SIZE, y * TILE_SIZE, resourse_manager)
                elif map[x][y] == '|':
                    self._board[x][y] = Tile('tower2', x * TILE_SIZE, y * TILE_SIZE, resourse_manager)
                elif map[x][y] == '$':
                    self._board[x][y] = Tile('tower3', x * TILE_SIZE, y * TILE_SIZE, resourse_manager)
                self._tile_group.add(self._board[x][y].get_sprite())


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
        self._tile_group.draw(surf)


pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
resource_manager = ResourceManager()
resource_manager.load_resources()
board = GameWorld(resource_manager)


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