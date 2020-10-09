from board import Board

class Game():
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.teams = {0: self.board.black, 1: self.board.white}

    def prompt(self):
        '''prompts the current player for input'''
        while True:
            choice = input(f'{self.teams[self.player()].color.capitalize()}, please enter a move in the form of start,finish (ex: a1,a3)\n')
            cols = list('abcdefgh')
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
                if self._check_move(move):
                    return move
                else:
                    print(f'{choice} is not a valid move')
        
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
            if piece.team is self.teams[self.player()]:
                if end_sq in piece.moves():
                    return True
        return False


    def show(self):
        '''Shows the board, round, and taken pieces'''
        print(self.board)
        print(f'Turn: {self.turn} - {self.teams[self.player()].color.capitalize()}\'s Turn')

    def take_turn(self):
        '''shows, prompts, does'''
        self.show()
        move = self.prompt()
        self.board.move(move)

g = Game()
for i in range(4):
    g.take_turn()
