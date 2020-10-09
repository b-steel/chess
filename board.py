from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from places import Captured, Square
from team import Team
class Board():
    def __init__(self):
        self.black = Team()
        self.white = Team()
        self.grid = {}
        self.dead_white = Captured()
        self.dead_black = Captured()

        self.white.opponent = self.black
        self.black.opponent = self.white
        self.create_squares()
        self.create_pieces()


    def create_pieces(self):
        for team, f_row, b_row, direction  in zip([self.black, self.white], [1, 6], [0, 7], [1, -1]):
            #pawns
            for col in range(8):
                p = Pawn(direction)
                team.add_piece(p)
                self.grid[f_row][col].add_piece(p)

            #rook
            for col in [0, 7]:
                p = Rook(direction)
                team.add_piece(p)
                self.grid[b_row][col].add_piece(p)

            #knight
            for col in [1, 6]:
                p = Knight(direction)
                team.add_piece(p)
                self.grid[b_row][col].add_piece(p)

            #bishop
            for col in [2, 5]:
                p = Bishop(direction)
                team.add_piece(p)
                self.grid[b_row][col].add_piece(p)
            
            #queen king
            for col, piece in zip([3,4], [Queen(direction), King(direction)]):
                team.add_piece(piece)      
                self.grid[b_row][col].add_piece(piece)


    def create_squares(self):
        for row in range(8):
            self.grid[row] = {}
            for col in range(8):
                self.grid[row][col] = Square()

        #neighbors
        #right
        for col in range(7):
            for row in range(8):
                self.grid[row][col].r = self.grid[row][col+1]
        #left
        for col in range(1,8):
            for row in range(8):
                self.grid[row][col].l = self.grid[row][col-1]
        #up
        for row in range(7):
            for col in range(8):
                self.grid[row][col].u = self.grid[row+1][col]
        #down
        for row in range(1, 8):
            for col in range(8):
                self.grid[row][col].d = self.grid[row-1][col]


    def capture(self, piece):
        '''adds piece to the captured list'''
        pass

    def move(self, move):
        '''Moves the piece from start to end'''
        pass


    def __str__(self):
        pass


        
