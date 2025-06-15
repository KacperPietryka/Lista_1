# -*- coding: utf-8 -*-
import pygame
from player import Player
from maps import tiles
from menu import Menu
from save_manager import SaveManager

pygame.init()

screen = pygame.display.set_mode((1800, 780))
pygame.display.set_caption("GRA")

menu = Menu()
player = Player()
sm = SaveManager()

sounds = pygame.mixer
channel = sounds.Channel(0)
music = sounds.Sound('music/base-music.wav')


# ladowanie gry
running = False

running = menu.load_game(screen, player)

restaurant = player.current_restaurant[1]
restaurat_copy = [restaurant]

clock = pygame.time.Clock()

while running:
    clock.tick(60)
    restaurant = player.current_restaurant[1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                menu.main_menu(screen)
            if event.key == pygame.K_b:
                player.buy_new_place(screen)
            if event.key == pygame.K_r:
                player.enter_restaurant(screen)
            if event.key == pygame.K_u:
                player.money = restaurant.upgrade(screen, player.money)
            if event.key == pygame.K_i:
                player.money = restaurant.buy(screen, player.money)
            if event.key == pygame.K_l:
                sm.load_game(player, screen)
            if event.key == pygame.K_s:
                sm.save_game(player, screen)
    screen.fill((0, 128, 255))
    for tile in tiles:
        tile.draw(screen)
    player.money += restaurant.events(screen)
    player.show_money(screen)
    if restaurant.music and not channel.get_busy():
        music.play()
    pygame.display.flip()

pygame.quit()
