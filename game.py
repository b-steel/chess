from board import Board
from pieces import King
WrongTeamError = 'That piece does not belong to you'
NoPieceError = 'There is no piece there\'t move there'
NotAMoveError = 'That piece cannot move there'
CheckError = 'That move would put you in Check'
class Game():
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.teams = {0: self.board.black, 1: self.board.white}
        self.loaded = False
    
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
        return self.teams[0].king.checkmate() or self.teams[1].king.checkmate()

    @property
    def in_check(self):
        b_king = self.teams[0].king
        w_king = self.teams[1].king
        return 'black' if b_king.check(b_king.place) else 'white' if w_king.check(w_king.place) else False

    def prompt(self):
        '''prompts the current player for input'''
        while True:
            choice = input(f'{self.teams[self.player()].color.capitalize()}, please enter a move in the form of start,finish (ex: a1,a3)\n')
            cols = list('abcdefgh')
            if choice.lower() == 'save':
                self.save_game()
                return 'save'
            else:
                try:
                    s,e = choice.lower().split(',')
                    scol, srow = list(s.lstrip().rstrip())
                    ecol, erow = list(e.lstrip().rstrip())
                    
                    assert scol in cols
                    assert ecol in cols
                    srow = int(srow)
                    erow = int(erow)
                    assert srow < 8
                    assert erow < 8
                    move =  ((scol, srow), (ecol, erow))
                    good = self._check_move(move)
                    if good is True:
                        return move
                    else:
                        print(good)
            
                except (ValueError, AssertionError) as e:
                    print(f'{choice} is not a valid input')

        

    def player(self):
        '''returns current player'''
        return self.turn%2

    def other(self):
        '''returns the other player'''
        return (self.turn + 1)%2

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
            else:
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
        self.board.move(move)
        self.turn +=1
        player_in_check = self.in_check
        if player_in_check:
            print(f'{player_in_check.capitalize()} is in CHECK')

    def play(self):
        if self.loaded:
            d = prompt('do you want to delete the file for the game you just loaded? Y/N\n')
            if d.lower == 'y':
                self.delete_file()

        while not self.game_over:
            r = self.take_turn()
            if r == 'save':
                break

        
        self.display_end_message() if self.game_over else print('\n')

        again = input('Do you want to play again??? Y/N\n')
        if again.lower() == 'y':
            return 'again'
        return 'done'

