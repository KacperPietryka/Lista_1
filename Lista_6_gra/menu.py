
import pygame
import os
import pickle

class Menu:
    def load_game(self, screen, player=''):
        options = ['About the author', 'Goal of the game',  'See best scores', 'Load game','START GAME']
        title = 'WELCOME TO THE GAME'
        index = self.menu_restaurant(screen, options, title=title)
        if index == 0:
            self.author(screen)
        elif index == 1:
            self.goal(screen)
        elif index == 2:
            self.show_best(screen)
        elif index == 3:
            from save_manager import SaveManager
            sm = SaveManager()
            sm.load_game(player, screen)
            return True
        elif index == 4:
            return True
        else:
            return False
        return self.load_game(screen)


    def show_best(self, screen):
        path = 'leaderboard/best.txt'
        data = []
        load_data = []
        if not os.path.exists(path):
            with open(path, 'wb') as f:
                for i in range(6):
                    pickle.dump([f'Player {i+1}', 0.0], f)
       
        with open(path, 'rb') as f:
            for _ in range(6):
                load_data.append(pickle.load(f))

        for record in load_data:
            data.append(f'{record[0]} ----> {record[1]}')

        self.menu_restaurant(screen, data, title='BEST SCORES')

    def author(self, screen):
        text = ['Game made by Kacper Pietryka', 'Student of the first year',
        'Studying at Politechnika Wroclawska (20 years old)']
        title = 'ABOUT THE AUTHOR'
        self.menu_restaurant(screen, text, title=title)
        

    def goal(self, screen):
        title='MAIN GOAL'
        text=['Buy all the available restaurants!',
             'Buy all possible upgrades', 'Have satisfied guests',
             'Have fun',]
        self.menu_restaurant(screen, text, title=title)
        
        
    def saved(self, screen):
        title='LIST OF ALL SAVED GAMES'
        text=[]
        self.menu_restaurant(screen, text, title=title)

    def main_menu(self, screen):
        title = 'MAIN MENU - to leave click any option below'
        options = ["Enter Restaurant - type R", "Buy New Restaurant - type B",
                   "Upgrade your Restaurant - type U", "Buy things for your Restaurant - type I",
                   "Save game - type S", "Load game - type L"]
        self.menu_restaurant(screen, options, title)

    def menu_restaurant(self, screen, options, title = ''):
        
        font = pygame.font.SysFont('Comic Sans MS', 48)
        selected = False
        chosen_index = None
        title_settings = font.render(title, True, (255, 255, 255))
        title_pos = title_settings.get_rect(center = (900,50))
        options.append('Leave')

        background = pygame.image.load('gallery/menu.png')
        background = pygame.transform.scale(background, (1800, 780))
        screen.blit(background, (0,0))

        # enables to move through menus
        while pygame.mouse.get_pressed()[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        while not selected:
            screen.blit(background, (0,0))
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            
            for index, option in enumerate(options):
                text_surface = font.render(option, True, (37, 232, 69))
                text_rect = text_surface.get_rect(topleft=(100, 100 + index * 60))
                
                if text_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (100, 100, 100), text_rect)
                    if mouse_click[0]:  
                        chosen_index = index
                        selected = True
                screen.blit(text_surface, text_rect.topleft)            
            screen.blit(title_settings, title_pos)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        if chosen_index == len(options) - 1: 
            return None # leave button problem
        else: 
            return chosen_index




