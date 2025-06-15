import pickle
import os, datetime
import pygame.font, pygame.event
import menu

pygame.font.init()
menu = menu.Menu()

class SaveManager():

    def manage_menu(self, screen, title, additional=False):
        text = []
        for i in range(4):
            text.append(f'Choose slot {i+1}')

        for i in range(4):
            path = f'saves/save_{i}/GameSave.pkl'
            if os.path.exists(path):
                edit = os.path.getmtime(path)
                date = datetime.datetime.fromtimestamp(edit)
                fixed_date = date.strftime('%Y-%m-%d %H:%M:%S')
                name = ''
                with open(path, 'rb') as f:
                    name = pickle.load(f)[0]
                text[i] = f'Player name: {name}, game saved: {fixed_date}!'
        if additional == True:
            text.append('WARNING - IF YOU SAVE IN FILE WHICH')
            text.append('IS ALREADY USED YOU WILL OVERWRITE IT')
        index = menu.menu_restaurant(screen, text, title)
        return index

    def get_player_name(self, screen):
        font = pygame.font.SysFont('Comic Sans MS', 60)
        t_font = pygame.font.SysFont('Comic Sans MS', 48)

        input_box = pygame.Rect(650, 375, 520, 100)
        color = pygame.Color((47, 245, 69))
        text = ''
        clock = pygame.time.Clock()

        title_settings = t_font.render('What is your name?', True, (255, 255, 255))
        title_pos = title_settings.get_rect(center = (900,50))

        background = pygame.image.load('gallery/menu.png')
        background = pygame.transform.scale(background, (1800, 780))

        while True:
            screen.blit(background, (0,0)) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 15:
                            text += event.unicode

            txt_surface = font.render(text, True, (255, 255, 255))

            screen.blit(txt_surface, (input_box.x + 5, input_box.y))
            screen.blit(title_settings, title_pos)

            pygame.draw.rect(screen, color, input_box, 4)
            pygame.display.flip()
            clock.tick(30)
    
    def change_leaderboard(self, score, name):
        data = []
        path = 'leaderboard/best.txt'

        if not os.path.exists(path):
            with open(path, 'wb') as f:
                for i in range(6):
                    pickle.dump([f'Player {i+1}', 0.0], f)

        with open(path, 'rb') as f:
            for _ in range(6):
                data.append(pickle.load(f))

        if score <= data[5][1]:
            return

        data[5][1] = score
        data[5][0] = name
        fixed_data = sorted(data, key=lambda x: x[1], reverse=True)

        with open(path, 'wb') as f:
            for i in fixed_data:
                pickle.dump(i, f)

    def save_game(self, player, screen):
        index = self.manage_menu(screen, 'Choose where you want to save your game', True)
        if index == None or index > 3:
            return

        name = self.get_player_name(screen)
        self.change_leaderboard(player.money, name)

        data = []
        data.append(name)
        data.append(player.money)
        data.append(player.restaurants)

        filename = f'saves/save_{index}/GameSave.pkl'
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

        

    def load_game(self, player, screen):
        index = self.manage_menu(screen, 'Choose which save you want to load')
        collect_data = []
        filename = f'saves/save_{index}/GameSave.pkl'
        if not os.path.exists(filename):
            return
        with open(filename, 'rb') as f:
            collect_data = pickle.load(f)

        player.money = collect_data[1]
        player.restaurants[2:]
        





