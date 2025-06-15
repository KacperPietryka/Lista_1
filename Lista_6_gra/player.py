import random
from maps import load_map
import pygame
from restaurant import Restaurant
from menu import Menu

pygame.init()
pygame.mixer.init()

sound = pygame.mixer
fail = sound.Sound('music/fail.wav')
success  = sound.Sound('music/success.wav')

option_restaurants = ['FastFood', 'Prestige', 'DrinkBar']
price_restaurant = [200, 50, 100]
client_state = ['positive', 'okay', 'angry', 'super_angry']

challenges = []
SIZE = 60

class Player():
    def __init__(self):
        self.money = 0.0
        self.no_restaurants = 1
        self.restaurants = [('rest1', Restaurant())]
        self.current_restaurant = [self.restaurants[0][0], self.restaurants[0][1]]
        load_map('rest1')
        self.menu = Menu()
    
    def buy_new_place(self, screen):
        text = []
        for index, restaurant in enumerate(option_restaurants):
            text.append(f'Buy a new {restaurant} restaurant - cost of {price_restaurant[index]} USD')
        chosen_index = self.menu.menu_restaurant(screen, text)

        if chosen_index is not None:
            restaurant = option_restaurants[chosen_index]
            cost = price_restaurant[chosen_index]
            if self.money >= cost:
                for k in self.restaurants:
                    if k[0] == restaurant:
                        fail.play()
                        return
                self.money -= cost
                self.restaurants.append((restaurant, Restaurant()))
                success.play()
            else:
                fail.play()
        return chosen_index

    def show_money(self, screen):
        font  = pygame.font.SysFont('Comic Sans MS', 48)
        text = font.render(f'Available money: {self.money}', True, (255, 255, 0))
        screen.blit(text, (20, 20))

    def enter_restaurant(self, screen):
        text = []
        for restaurant in self.restaurants:
            text.append(f'Enter the restaurant: {restaurant[0]}')
        chosen_index = self.menu.menu_restaurant(screen, text, title=
        'Choose restaurant you want to enter')
        if chosen_index is not None:
            res_pos = self.restaurants[chosen_index][1]
            name = self.restaurants[chosen_index][0]
            self.current_restaurant = [name, res_pos]
            load_map(name)  
        return chosen_index

pygame.quit()
