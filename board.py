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
        self.cols = list('abcdefgh')

        self.white.opponent = self.black
        self.black.opponent = self.white
        self.create_squares()
        self.create_pieces()


    def create_pieces(self):
        for team, f_row, b_row, direction  in zip([self.black, self.white], [1, 6], [0, 7], [1, -1]):
            #pawns
            for col in self.cols:
                p = Pawn(direction)
                team.add_piece(p)
                self.grid[col][f_row].add_piece(p)

            #rook
            for col in ['a', 'h']:
                p = Rook(direction)
                team.add_piece(p)
                self.grid[col][b_row].add_piece(p)

            #knight
            for col in ['b', 'g']:
                p = Knight(direction)
                team.add_piece(p)
                self.grid[col][b_row].add_piece(p)

            #bishop
            for col in ['c', 'f']:
                p = Bishop(direction)
                team.add_piece(p)
                self.grid[col][b_row].add_piece(p)
            
            #queen king
            for col, piece in zip(['d', 'e'], [Queen(direction), King(direction)]):
                team.add_piece(piece)      
                self.grid[col][b_row].add_piece(piece)
                if isinstance(piece, King):
                    team.king = piece
                    piece.board = self


    def create_squares(self):
        cols = self.cols
        for col in cols:
            self.grid[col] = {}
            for row in range(8):
                sq = Square()
                sq.row = row
                sq.col = col
                self.grid[col][row] = sq


        #neighbors
        #right
        for i,col in enumerate(cols[:7]):
            for row in range(8):
                self.grid[col][row].r = self.grid[cols[i+1]][row]
        #left
        for i,col in enumerate(cols[1:8]):
            for row in range(8):
                self.grid[col][row].l = self.grid[cols[i]][row]
        #up
        for row in range(7):
            for col in cols:
                self.grid[col][row].u = self.grid[col][row+1]
        #down
        for row in range(1, 8):
            for col in cols:
                self.grid[col][row].d = self.grid[col][row-1]


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
        t = self.teams[self.player]
        
        if end in p.moves():
            return True
        return False


    def move(self, move):
        '''Moves the piece from start to end. Assumes valid move
        
        move is (start(col, row), end(col, row))'''
        start = self.grid[move[0][0]][move[0][1]]
        end = self.grid[move[1][0]][move[1][1]]
        p = start.piece
        p.moved = True
        if end.piece:
            if isinstance(p, King) and isinstance(end.piece, Rook) and p.team == end.piece.team and not end.piece.moved:
                #castle
                start.add_piece(end.piece) #put castle in king spot
                end.add_piece(p) # put king in castle spot
            else:  
                self.capture(end.piece)
                end.add_piece(p)
                start.piece = None
        else:
            end.add_piece(p)
            start.piece = None
        
    def get_text(self, col, row):
        return self.grid[col][row].piece.char if self.grid[col][row].piece else '+'

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
            for col in list('abcdefgh'):
                s += f'{{self.get_text(\'{col}\',{row})}}'
                if col != 'h':
                    s += ' '
            s +=f'|{row}  {{d_w[{row*2}]}} {{d_w[{row*2+1}]}}\n'
        s += f'         a b c d e f g h'

        d_w = self.get_dead('w')
        d_b = self.get_dead('b')

        text =  f"Taken    a b c d e f g h    Taken\n{d_b[0]} {d_b[1]}    7|{self.get_text('a',7)} {self.get_text('b',7)} {self.get_text('c',7)} {self.get_text('d',7)} {self.get_text('e',7)} {self.get_text('f',7)} {self.get_text('g',7)} {self.get_text('h',7)}|7  {d_w[14]} {d_w[15]}\n{d_b[2]} {d_b[3]}    6|{self.get_text('a',6)} {self.get_text('b',6)} {self.get_text('c',6)} {self.get_text('d',6)} {self.get_text('e',6)} {self.get_text('f',6)} {self.get_text('g',6)} {self.get_text('h',6)}|6  {d_w[12]} {d_w[13]}\n{d_b[4]} {d_b[5]}    5|{self.get_text('a',5)} {self.get_text('b',5)} {self.get_text('c',5)} {self.get_text('d',5)} {self.get_text('e',5)} {self.get_text('f',5)} {self.get_text('g',5)} {self.get_text('h',5)}|5  {d_w[10]} {d_w[11]}\n{d_b[6]} {d_b[7]}    4|{self.get_text('a',4)} {self.get_text('b',4)} {self.get_text('c',4)} {self.get_text('d',4)} {self.get_text('e',4)} {self.get_text('f',4)} {self.get_text('g',4)} {self.get_text('h',4)}|4  {d_w[8]} {d_w[9]}\n{d_b[8]} {d_b[9]}    3|{self.get_text('a',3)} {self.get_text('b',3)} {self.get_text('c',3)} {self.get_text('d',3)} {self.get_text('e',3)} {self.get_text('f',3)} {self.get_text('g',3)} {self.get_text('h',3)}|3  {d_w[6]} {d_w[7]}\n{d_b[10]} {d_b[11]}    2|{self.get_text('a',2)} {self.get_text('b',2)} {self.get_text('c',2)} {self.get_text('d',2)} {self.get_text('e',2)} {self.get_text('f',2)} {self.get_text('g',2)} {self.get_text('h',2)}|2  {d_w[4]} {d_w[5]}\n{d_b[12]} {d_b[13]}    1|{self.get_text('a',1)} {self.get_text('b',1)} {self.get_text('c',1)} {self.get_text('d',1)} {self.get_text('e',1)} {self.get_text('f',1)} {self.get_text('g',1)} {self.get_text('h',1)}|1  {d_w[2]} {d_w[3]}\n{d_b[14]} {d_b[15]}    0|{self.get_text('a',0)} {self.get_text('b',0)} {self.get_text('c',0)} {self.get_text('d',0)} {self.get_text('e',0)} {self.get_text('f',0)} {self.get_text('g',0)} {self.get_text('h',0)}|0  {d_w[0]} {d_w[1]}\n         a b c d e f g h"


        return text

    def __str__(self):
        return self._print_text()


# b = Board()
# b.move((('a',1), ('a',3)))
# b.capture(b.grid['a'][0].piece)
# b.capture(b.grid['h'][6].piece)
# print(b.grid['b'][0])
# print(b.grid['b'][0].piece)

# print(b)

        
