# -*- coding: utf-8 -*-
import pygame

pygame.init()

screen = pygame.display.set_mode((1800, 780))
pygame.display.set_caption("Kreator map")

size = 60
rows = 13
cols = 30
tiles = []

possible_colors = [(156, 192, 144), (204, 147, 116), (33, 69, 68), (33, 207, 216),
                   (104, 107, 129), (65, 55, 229), (245, 219, 64)]

class Tile:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.colors = possible_colors
        self.color_index = 0
        self.color = self.colors[self.color_index]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)  # siatka

    def next_color(self):
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.color = self.colors[self.color_index]
    
    def load_color(self, id_):
        self.color_index = id_
        self.color = self.colors[self.color_index]

def save():
    x = input('nazwa mapy')
    with open(f'maps/{x}.txt', 'w') as file_:
        for tile in tiles:
            color = tile.color_index
            file_.write(str(color))
    print('File saved!')

def create():
    for row in range(rows):
        for col in range(cols):
            x = col * size
            y = row * size
            tiles.append(Tile(x, y, size))

def load_map(map_name):
    global tiles
    tiles.clear()
    create()
    with open(f'maps/{map_name}.txt', 'r') as f:
        for tile in tiles:
            index = f.read(1)
            tile.load_color(int(index))

create()
running = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print('Saving game...')
                save()
            elif event.key == pygame.K_l:
                print('loading game...')
                load_map('rest1')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for tile in tiles:
                if tile.rect.collidepoint(mouse_pos):
                    tile.next_color()

    screen.fill((0, 128, 255))

    for tile in tiles:
        tile.draw(screen)
    pygame.display.flip()

pygame.quit()
        




