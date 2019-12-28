import pygame
import os

DISPLAY_SIZE = (2000, 1000)


class Board:

    def __init__(self, width, height, x=10, y=10, cell_size=30):
        self._width = width
        self._height = height
        self._x = x
        self._y = y
        self._board = [[0] * height for _ in range(width)]
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


print()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def load_level(map):
        map.txt = "C:\\Users\\Пользователь\\PycharmProjects\\untitled1\\data\\map.txt"
        with open(map.txt, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

    def load_image(name):
        fullname = os.path.join('data')
        tile_images = {'wall': pygame.image.load('tree.jpg'), 'for_towers': pygame.image.load('grass.jpg'),
                       'road': pygame.image.load('sand.jpg'), 'tron': pygame.image.load('tron.jpg')}
        tile_images = pygame.image.load(fullname).convert()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()

    def generate_level(level):
        x, y = None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('for_towers', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '&':
                    Tile('road', x, y)
                elif level[y][x] == '%':
                    Tile('tron', x, y)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)

    screen.fill((0, 0, 0))
    level_x, level_y = generate_level(load_level('map.txt'))
    board.draw(screen)
    pygame.display.flip()

pygame.quit()