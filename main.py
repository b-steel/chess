from game import Game
import pickle
import os
from colors import color, text_colors
class GameRunner():
    def __init__(self):
        self.game = None


    def load_game(self):
        files = []
        for (dirpath, dirnames, filenames) in os.walk('.saved-games'):
            files.extend(filenames)
            break
        if files:
            print('The following saved games are available:')
            for (i, g) in enumerate(files):
                print(f'Choose {i} to select: ', f'{g[0:-7]}')
            i = input('\nWhich Game would you like to load?\n')
            if int(i) < len(files):
                with open(f'.saved-games/{files[int(i)]}', 'rb') as f:
                    self.game = pickle.load(f)
                    print('File Loaded\n')
            else:
                print('Invalid Choice')
        else:
            print('There are no saved games')
        
    def delete_game(self):
        files = []
        for (dirpath, dirnames, filenames) in os.walk('.saved-games'):
            files.extend(filenames)
            break
        if files:
            print('The following saved games are available:')
            for (i, g) in enumerate(files):
                print(f'Choose {i} to select: ', f'{g[0:-7]}')
            i = input('\nWhich Game would you like to delete?\n')
            if int(i) < len(files):
                os.remove(f'.saved-games/{files[int(i)]}')
                print('File Deleted\n')     
            else:
                print('Invalid Choice')
        else:
            print('There are no saved games')
        
if __name__ == '__main__':

    gr = GameRunner()
    running = True
    i = ''
    while running:
        if i.lower() == 'done':
            break
        i = input('\nPlease choose a mode <new>, <load>, or <delete>\n')
        if i.lower() == 'new':
            gr.game = Game()
            i = gr.game.play()
        elif i.lower() == 'load':
            gr.load_game()
            if gr.game:
                i = gr.game.play()
        elif i.lower() == 'delete':
            gr.delete_game()
        else: 
            print(f'{colors.color("That is not a valid command, please try again", "RED")}')