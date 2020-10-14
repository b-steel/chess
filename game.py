from board import Board
from pieces import King, Rook
from move import Move
import pickle
import os
import re
WrongTeamError = 'That piece does not belong to you'
NoPieceError = 'There is no piece there'
NotAMoveError = 'That piece cannot move there'
CheckError = 'That move would put you in Check'

class Game():
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.players = {1: self.board.black, 0: self.board.white}
   
    def delete_file(self):
        os.remove(f'.saved-games/{self.loaded}')

    def save_game(self):
        files = []
        for (dirpath, dirnames, filenames) in os.walk('.saved-games'):
            files.extend(filenames)
            break
        file_num = 0
        for f in files:
            m = re.search('_(\d+)\.pickle', f)
            if m:
                found = m.group(1)
                if int(found) > file_num:
                    file_num = int(found)
        file_num+=1
        with open(f'.saved-games/chess_{str(file_num)}.pickle', 'wb') as f:
            pickle.dump(self, f)
        print(f'GAME SAVED as chess_{file_num}')

    @property
    def game_over(self):
        return self.board.rulechecker.checkmate

    @property
    def in_check(self):
        return self.board.rulechecker.check

    @property    
    def player(self):
        '''returns current player'''
        return self.players[self.turn%2]

    @property
    def other(self):
        '''returns the other player'''
        return self.players[(self.turn + 1)%2]

    def parse_input(self, inp):
        cols = list('abcdefgh')
        try:
            if ',' in inp:
                s,e = inp.lower().split(',')
            elif ' ' in inp:
                s,e = inp.lower().split(' ')
            else:
                raise ValueError
            scol, srow = list(s.lstrip().rstrip())
            ecol, erow = list(e.lstrip().rstrip())
            
            assert scol in cols
            assert ecol in cols
            srow = int(srow)
            erow = int(erow)
            assert srow < 8
            assert erow < 8
            return Move(self.board.grid[scol][srow], self.board.grid[ecol][erow])
        
        except (ValueError, AssertionError) as e:
            return None
    
    def _check_move(self, move):
        '''Check if the piece belongs to the player and is valid'''
        start = move.start 
        end = move.end
        piece = move.piece
    
        if piece:    
            if piece.player is self.player:
                if end in piece.available_moves(self.board):
                    return True
                else:
                    return NotAMoveError
            else: 
                return WrongTeamError
        else:
            return NoPieceError

    def prompt(self):
        '''prompts the current player for input'''
        while True:
            choice = input(f'{self.player.color.capitalize()}, please enter a move:\n')
            if choice.lower() == 'save':
                return 'save'
            elif choice.lower() == 'exit':
                return 'exit'
            else:
                move = self.parse_input(choice)
                if move:
                    good = self._check_move(move)
                    if good is True:
                        return move
                    else:
                        print(good)
                else:
                    print(f'{choice} is not a valid input')

    def display_end_message(self):
        print(f'{self.player[self.other]} is the Winner!')

    def show(self):
        '''Shows the board, round, and taken pieces'''
        print(self.board)
        print(f'Turn: {self.turn} - {self.player.color.capitalize()}\'s Turn')

    def take_turn(self):
        '''shows, prompts, does'''
        self.show()
        move = self.prompt()
        if not isinstance(move, Move):
            return move
        self.board.move(move)
        self.turn += 1

        player_in_check = self.in_check
        if player_in_check:
            if self.game_over:
                pass
            else:
                print(f'{player_in_check.capitalize()} is in CHECK')

    def play(self):
        while not self.game_over:
            r = self.take_turn()
            if r == 'save':
                self.save_game()
                break
            elif r == 'exit':
                break
        
        self.display_end_message() if self.game_over else print('\n')

        again = input('Do you want to play again??? Y/N\n')
        if again.lower() == 'y':
            return 'again'
        return 'done'
