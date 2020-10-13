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
    class RuleChecker():
        def __init__(self, board):
            self.board = board
            self.white = board.white
            self.black = board.black

        @property
        def checkmate(self):
            def in_checkmate(player):
                def threats(king):
                    '''Returns the piece(s) that has/have the king in check'''
                    p = []
                    for piece in king.player.opponent.pieces:
                        if king.place in piece.moves():
                            return p.append(piece)
                    return p
                
                def move_out_of_check(king):
                    #can the king move out of danger
                    for mv in king.moves():
                        if not king.check(mv):
                            return True
                    return False
                
                king = player.king
                if move_out_of_check(king):
                    return False

                threat_pieces = threats(player.king)
                if threat_pieces:
                    if len(threat_pieces) == 1:
                        threat = threat_pieces[0]
                        for piece in player.pieces:
                            #can one of my pieces take out the threat piece
                            if threat.place in piece.moves():
                                return False
                            elif isinstance(threat_piece, (Bishop, Rook, Queen)):
                                #can a piece block the threat
                                for destination in piece.moves():
                                    if destination.piece:
                                        #we only care about blank spaces
                                        pass
                                    else:
                                        to_return = piece.place
                                        test_move = Move(piece, to_return, destination)
                                        reverse_move = Move(piece, destination, to_return)
                                        self.move(test_move)
                                        if not king.check():
                                            self.move(reverse_move)
                                            return False
                                        self.move(reverse_move)
                    else:
                        #double check, only way out is with the king moving, we took care of that above
                        pass       
                return True
            if in_checkmate(self.black):
                return self.black
            elif in_checkmate(self.white):
                return self.white
            return None

        @property
        def check(self):
            def in_check(player):
                if player.king.check(player.king.place):
                    return True
                return False
            if in_check(self.white):
                return self.white
            elif in_check(self.black):
                return self.black
            return None

    
        def en_passant_capture(self):
            move = self.board.last_turn
            piece = move.piece
            if isinstance(piece, Pawn):
                if move.start.col != move.end.col: #diagonal == capture
                    if not move.capture: #no piece caputured
                        if piece.player.direction == 1:
                            caputured_pawn = move.end.d.piece
                        else:
                            caputured_pawn = move.end.u.piece
                        #set the record straight in the history
                        move.capture = caputured_pawn
                        move.piece.player.capture(caputured_pawn)
    
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.rulechecker = RuleChecker(self)
        self.players = {1: self.board.black, 2: self.board.white}
   
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
        return self.rulechecker.checkmate

    @property
    def in_check(self):
        return self.rulechecker.check

    @property    
    def player(self):
        '''returns current player'''
        return self.players[self.turn%2 +1]

    @property
    def other(self):
        '''returns the other player'''
        return self.players[(self.turn + 1)%2 + 1]

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
                if end in piece.moves():
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
        if move == 'save':
            return 'save'
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

        
        self.display_end_message() if self.game_over else print('\n')

        again = input('Do you want to play again??? Y/N\n')
        if again.lower() == 'y':
            return 'again'
        return 'done'

