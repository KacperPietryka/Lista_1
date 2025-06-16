import pygame
import time
import random
from functools import partial
from menu import Menu


SIZE = 60
pygame.init()
pygame.mixer.init()
menu = Menu()

sounds = pygame.mixer
fail = sounds.Sound('music/fail.wav')
money_sound = sounds.Sound('music/money-sound.wav')
music = sounds.Sound('music/base-music.wav')
success = sounds.Sound('music/success.wav')

possible_upgrades = ['Improve the quality of staff',
                    'increase popularity of a restaurant - more guests',
                    'Hire more staff (max 5 people)']
possible_buys = ['new oven', 'add music', 
                 'buy a new door', 'better refrigerator']

buy_cost = [100, 10, 500, 40] # mozna edytowac


def icon(screen, X, Y, icon, height = SIZE, length = SIZE): # method to draw icons
    image = pygame.image.load(f'gallery/{icon}.png')
    scaled_image = pygame.transform.scale(image, (height, length))
    active = pygame.Rect(X, Y, height, length)
    pygame.draw.rect(screen, 'white', active, 1)
    screen.blit(scaled_image, (X, Y))

class Restaurant():
    def __init__(self):
        self.stats = [1, 1, 1] # better staff quality, popularity, more staff        
        self.income_float = 1
        self.your_upgrades = []
        self.coin_spawn_time = None
        self.guest_time = time.time()
        self.x = 0
        self.y = 0
        self.icons = []
        self.guests = []
        self.music = False
    
    def upgrade(self, screen, money):
        text = []
        index = 0
        for purchase in possible_upgrades:
            payment = self.stats[index] * 2
            text.append(f'{purchase} - cost of {payment} lvl {self.stats[index]}/5')
            index += 1
        decision = menu.menu_restaurant(screen, text, title = 'Improve your Restaurant!')
        if decision is None:
           fail.play()
           return money

        payment = self.stats[decision] * 2

        if self.stats[decision] >= 5:
            fail.play()
        elif money >= payment:
            success.play()
            money -= payment
            self.stats[decision] += 1
        return money

    def buy(self, screen, money):
        text = []
        index = 0

        for purchase in possible_buys:
            payment = buy_cost[index]
            text.append(f'{purchase} - cost of {payment}')
            index += 1

        pick = menu.menu_restaurant(screen, text, title='Buy more stuff for your Restaurant!')
        if pick is None:
            return money # obsluga opcji leave
        inventory = self.your_upgrades
        expense = buy_cost[pick]
        bought = possible_buys[pick]
        if expense <= money and bought not in inventory:
            money -= expense
            self.your_upgrades.append(bought)
            self.build(screen, bought)
            if bought == 'add music':
                self.music = True
            success.play()
        else:
            fail.play()
        return money
    
    def build(self, screen, bought = ''):
        place = self.icons
        if bought == 'add music':
            place.append(partial(icon, screen, 17 * SIZE, 2 * SIZE, 'music', 3*SIZE, 2*SIZE))
        elif bought == 'new oven':
            place.append(partial(icon, screen, 25 * SIZE, 2 * SIZE, 'oven'))
        elif bought == 'buy a new door':
            place.append(partial(icon, screen, 23 * SIZE, 7 * SIZE, 'door'))
        elif bought == 'better refrigerator':
            place.append(partial( icon, screen, 27 * SIZE, 2 * SIZE, 'refrigerator'))

    def show_clients(self, screen):
        current_time = time.time()
        if current_time - self.guest_time >= 5:
            self.guest_time = current_time
            no_guests = self.stats[1] * 3
            self.guests = []
            data = self.clients()
            a, b = zip(*data)
            size = len(a)
            used = []
            for i in range(no_guests):
                guest = i % 3 # icon of guest
                while True:
                    pos = random.randint(0, size-1)
                    if pos not in used:
                        break
                self.guests.append((a[pos], b[pos], guest))
        for guest in self.guests: # displaying all the guests
            x,y, image = guest
            icon(screen, x* SIZE, y * SIZE, f'guest{image}')

    def clients(self):
        blocks = []
        with open('maps/rest1.txt', 'r') as f:
            colors = f.read()
            for pos in range(len(colors)):
                if colors[pos] == '2':
                    x = pos % 30
                    y = pos // 30
                    if x > 0 and 1 < y < 12:
                        blocks.append([x, y])
        return blocks
    
    def show_upgrades(self):
        for item in self.icons: # displaying all the icons
            item()

    def events(self, screen):
        balance = 0.0
        self.show_clients(screen)
        self.show_upgrades()
        balance += self.earn(screen)
        return balance

    def earn(self, screen):
        current_time = time.time()
        if self.coin_spawn_time is None or (current_time - self.coin_spawn_time >= 2):
            self.x = random.randint(1, 20) * SIZE
            self.y = random.randint(1, 10) * SIZE
            self.coin_spawn_time = current_time
        coin = self.stats[0] # benefits if better level
        self.income_float = (self.stats[0] * 5)

        active = pygame.Rect(self.x, self.y, SIZE, SIZE)
        icon(screen, self.x, self.y, f'money{coin}')
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] and active.collidepoint(mouse_pos):
            money_sound.play()
            self.coin_spawn_time = None
            return self.income_float
        
        return 0
pygame.quit()


