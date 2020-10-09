from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from places import Captured, Square
from team import Team
class Board():
    def __init__(self):
        self.black = Team('black')
        self.white = Team('white')
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
        if piece.team is self.black:
            self.dead_black.add_piece(piece)
        else:
            self.dead_white.add_piece(piece)

    def check_move(self, move):
        start = self.grid[move[0][0]][move[0][1]]
        end = self.grid[move[1][0]][move[1][1]]
        p = start.piece
        if end in p.moves():
            return True
        return False


    def move(self, move):
        '''Moves the piece from start to end. Assumes valid move
        
        move is (start(col, row), end(col, row))'''
        start = self.grid[move[0][1]][move[1][0]]
        end = self.grid[move[1][1]][move[1][0]]
        p = start.piece
        if end.piece:
            self.capture(end.piece)
        end.add_piece(p)
        start.piece = None
        
    def get_text(self, row, col):
        return self.grid[row][col].piece.char if self.grid[row][col].piece else '+'

    def get_dead(self, color):
        if color == 'b':
            p = self.dead_black.pieces + [None]*(16-len(self.dead_black.pieces))
        else:
            p = self.dead_white.pieces + [None]*(16-len(self.dead_white.pieces))
        return [piece.char if piece else ' ' for piece in p]
        
    def _print_text(self):

        #It's gonna get MESSY lookin'
        s = 'Taken    a b c d e f g h    Taken\n'
        for row in range(7, -1, -1):
            s += f'{{d_b[{(7-row)*2}]}} {{d_b[{(7-row)*2+1}]}}    {row}|'
            for col in range(8):
                s += f'{{self.get_text({row},{col})}}'
                if col != 7:
                    s += ' '
            s +=f'|{row}  {{d_w[{row*2}]}} {{d_w[{row*2+1}]}}\n'
        s += f'         a b c d e f g h'

        d_w = self.get_dead('w')
        d_b = self.get_dead('b')

        text =  f'Taken    a b c d e f g h   Taken\n{d_b[0]} {d_b[1]}    7|{self.get_text(7,0)} {self.get_text(7,1)} {self.get_text(7,2)} {self.get_text(7,3)} {self.get_text(7,4)} {self.get_text(7,5)} {self.get_text(7,6)} {self.get_text(7,7)}|7  {d_w[14]} {d_w[15]}\n{d_b[2]} {d_b[3]}    6|{self.get_text(6,0)} {self.get_text(6,1)} {self.get_text(6,2)} {self.get_text(6,3)} {self.get_text(6,4)} {self.get_text(6,5)} {self.get_text(6,6)} {self.get_text(6,7)}|6  {d_w[12]} {d_w[13]}\n{d_b[4]} {d_b[5]}    5|{self.get_text(5,0)} {self.get_text(5,1)} {self.get_text(5,2)} {self.get_text(5,3)} {self.get_text(5,4)} {self.get_text(5,5)} {self.get_text(5,6)} {self.get_text(5,7)}|5  {d_w[10]} {d_w[11]}\n{d_b[6]} {d_b[7]}    4|{self.get_text(4,0)} {self.get_text(4,1)} {self.get_text(4,2)} {self.get_text(4,3)} {self.get_text(4,4)} {self.get_text(4,5)} {self.get_text(4,6)} {self.get_text(4,7)}|4  {d_w[8]} {d_w[9]}\n{d_b[8]} {d_b[9]}    3|{self.get_text(3,0)} {self.get_text(3,1)} {self.get_text(3,2)} {self.get_text(3,3)} {self.get_text(3,4)} {self.get_text(3,5)} {self.get_text(3,6)} {self.get_text(3,7)}|3  {d_w[6]} {d_w[7]}\n{d_b[10]} {d_b[11]}    2|{self.get_text(2,0)} {self.get_text(2,1)} {self.get_text(2,2)} {self.get_text(2,3)} {self.get_text(2,4)} {self.get_text(2,5)} {self.get_text(2,6)} {self.get_text(2,7)}|2  {d_w[4]} {d_w[5]}\n{d_b[12]} {d_b[13]}    1|{self.get_text(1,0)} {self.get_text(1,1)} {self.get_text(1,2)} {self.get_text(1,3)} {self.get_text(1,4)} {self.get_text(1,5)} {self.get_text(1,6)} {self.get_text(1,7)}|1  {d_w[2]} {d_w[3]}\n{d_b[14]} {d_b[15]}    0|{self.get_text(0,0)} {self.get_text(0,1)} {self.get_text(0,2)} {self.get_text(0,3)} {self.get_text(0,4)} {self.get_text(0,5)} {self.get_text(0,6)} {self.get_text(0,7)}|0  {d_w[0]} {d_w[1]}\n         a b c d e f g h'




        return text

    def __str__(self):
        return self._print_text()


# b = Board()
# b.move(((1,0), (3,0)))
# b.capture(b.grid[0][6].piece)
# b.capture(b.grid[7][5].piece)
# b.capture(b.grid[7][0].piece)
# b.capture(b.grid[1][5].piece)
# b.capture(b.grid[1][3].piece)
# b.capture(b.grid[1][1].piece)
# b.capture(b.grid[1][7].piece)

# print(b)

        
