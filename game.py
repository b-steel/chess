from board import Board
from pieces import King, Rook
WrongTeamError = 'That piece does not belong to you'
NoPieceError = 'There is no piece there'
NotAMoveError = 'That piece cannot move there'
CheckError = 'That move would put you in Check'
class Game():
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.teams = {1: self.board.black, 2: self.board.white}
        self.loaded = False
        self.gameover = False

    
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
        return self.teams[1].king.checkmate() or self.teams[2].king.checkmate()

    @property
    def in_check(self):
        b_king = self.teams[1].king
        w_king = self.teams[2].king
        return 1 if b_king.check(b_king.place) else (2 if w_king.check(w_king.place) else False)

    def prompt(self):
        '''prompts the current player for input'''
        while True:
            choice = input(f'{self.teams[self.player()].color.capitalize()}, please enter a move in the form of start,finish (ex: a1,a3) or start finish (ex: b4 g2)\n')
            if choice.lower() == 'save':
                self.save_game()
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

        

    def player(self):
        '''returns current player'''
        return self.turn%2 +1

    def other(self):
        '''returns the other player'''
        return (self.turn + 1)%2 + 1
    
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
            return ((scol, srow), (ecol, erow))
        
    
        except (ValueError, AssertionError) as e:
            return None

    def _check_move(self, move):
        '''Check if the piece belongs to the player and is valid'''
        s,e = move
        scol,srow = s
        ecol, erow = e
        start_sq = self.board.grid[scol][srow]
        
        piece = start_sq.piece
        end_sq = self.board.grid[ecol][erow]
    
        if piece:
            if isinstance(piece, King):
                if piece.check(end_sq):
                    return CheckError
                elif isinstance(end_sq.piece, Rook) and end_sq.piece.team == piece.team and not end_sq.piece.moved and not piece.moved:
                    return True

            if piece.team is self.teams[self.player()]:
                if end_sq in piece.moves():
                    return True
                else:
                    return NotAMoveError
            else: 
                return WrongTeamError
        else:
            return NoPieceError

    def display_end_message(self):
        print(f'{self.teams[self.other]} is the Winner!')

    def show(self):
        '''Shows the board, round, and taken pieces'''
        print(self.board)
        print(f'Turn: {self.turn} - {self.teams[self.player()].color.capitalize()}\'s Turn')

    def take_turn(self):
        '''shows, prompts, does'''
        self.show()
        move = self.prompt()
        if move == 'save':
            return 'save'
        self.do(move)
    
    def do(self, move):
        self.board.move(move)
        self.turn +=1
        player_in_check = self.in_check
        if player_in_check:
            if self.teams[player_in_check].king.checkmate():
                self.gameover = True
            else:
                print(f'{player_in_check.capitalize()} is in CHECK')


    def play(self):
        if self.loaded:
            d = prompt('do you want to delete the file for the game you just loaded? Y/N\n')
            if d.lower == 'y':
                self.delete_file()
        while not self.gameover:
            r = self.take_turn()
            if r == 'save':
                break

        
        self.display_end_message() if self.game_over else print('\n')

        again = input('Do you want to play again??? Y/N\n')
        if again.lower() == 'y':
            return 'again'
        return 'done'

