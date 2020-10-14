from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from places import Square
from player import Player
from copy import deepcopy
from move import Move
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
                    if king.place in piece.available_moves(self.board):
                        return p.append(piece)
                return p
            
            def move_out_of_check(king):
                #can the king move out of danger
                for sq in king.available_moves(self.board):
                    if not king.check(sq, self.board):
                        return True
                return False
            
            def between (place, start, end):
                cols = list('abcdefgh')
                if start.row <= place.row <= end.row or end.row <= place.row <= start.row:
                    pcol = cols.index(place.col)
                    scol = cols.index(start.col)
                    ecol = cols.index(end.col)
                    if scol <= pcol <= ecol or ecol <= pcol <= scol:
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
                        if threat.place in piece.available_moves(self.board):
                            return False
                        elif isinstance(threat_piece, (Bishop, Rook, Queen)):
                            #can a piece block the threat
                            for destination in piece.available_moves(self.board):
                                if destination.piece:
                                    #we only care about blank spaces
                                    pass
                                elif between(destination, threat.place, king.place):
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
            if player.king.check(player.king.place, self.board):
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

class Board():
    def __init__(self):
        self.black = Player('black')
        self.white = Player('white')
        self.grid = {}
        self.cols = list('abcdefgh')
        self.white.opponent = self.black
        self.black.opponent = self.white
        self.moves = {}
        self.rulechecker = RuleChecker(self)
        self.create_squares()
        self.create_pieces()

    @property
    def last_turn(self):
        return self.moves[len(self.moves)-1]

    def create_squares(self):
        cols = self.cols
        for col in cols:
            self.grid[col] = {}
            for row in range(8):
                self.grid[col][row] = Square(col, row)

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

    def create_pieces(self):
        for player, f_row, b_row  in zip([self.white, self.black], [1, 6], [0, 7]):
            #pawns
            for col in self.cols:
                p = Pawn(player)
                if player == self.black:
                    p.direction = -1
                player.add_piece(p)
                self.grid[col][f_row].add_piece(p)

            #rook
            for col in ['a', 'h']:
                p = Rook(player)
                player.add_piece(p)
                self.grid[col][b_row].add_piece(p)

            #knight
            for col in ['b', 'g']:
                p = Knight(player)
                player.add_piece(p)
                self.grid[col][b_row].add_piece(p)

            #bishop
            for col in ['c', 'f']:
                p = Bishop(player)
                player.add_piece(p)
                self.grid[col][b_row].add_piece(p)
            
            #queen king
            for col, piece in zip(['d', 'e'], [Queen(player), King(player)]):
                player.add_piece(piece)      
                self.grid[col][b_row].add_piece(piece)
                if isinstance(piece, King):
                    player.king = piece
   
    def move(self, move):
        '''Moves the piece from start to end. Assumes valid move
        
        move is instance of Move class'''

        start = move.start
        end = move.end
        piece = move.piece
        assert piece is start.piece

        piece.moved = True
        if end.piece:
            if isinstance(piece, King) and not piece.moved and isinstance(end.piece, Rook) and piece.player == end.piece.team and not end.piece.moved:
                #castle
                start.add_piece(end.piece) #put castle in king spot
            else:  
                piece.player.capture(end.piece) #Capture it
                start.piece = None
        else:
            start.piece = None
        end.add_piece(piece) #put the piece 
        self.moves[len(self.moves)] = move # store the move
        self.rulechecker.en_passant_capture() #check for en passant

        
    def get_text(self, col, row):
        return self.grid[col][row].piece.char if self.grid[col][row].piece else '+'

    def get_dead(self, color):
        if color == 'b':
            p = self.white.captured + [None]*(16-len(self.white.captured))
        else:
            p = self.black.captured + [None]*(16-len(self.black.captured))
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

        text =  f"Taken    a b c d e f g h    Taken\n{d_w[0]} {d_w[1]}    7|{self.get_text('a',7)} {self.get_text('b',7)} {self.get_text('c',7)} {self.get_text('d',7)} {self.get_text('e',7)} {self.get_text('f',7)} {self.get_text('g',7)} {self.get_text('h',7)}|7  {d_b[14]} {d_b[15]}\n{d_w[2]} {d_w[3]}    6|{self.get_text('a',6)} {self.get_text('b',6)} {self.get_text('c',6)} {self.get_text('d',6)} {self.get_text('e',6)} {self.get_text('f',6)} {self.get_text('g',6)} {self.get_text('h',6)}|6  {d_b[12]} {d_b[13]}\n{d_w[4]} {d_w[5]}    5|{self.get_text('a',5)} {self.get_text('b',5)} {self.get_text('c',5)} {self.get_text('d',5)} {self.get_text('e',5)} {self.get_text('f',5)} {self.get_text('g',5)} {self.get_text('h',5)}|5  {d_b[10]} {d_b[11]}\n{d_w[6]} {d_w[7]}    4|{self.get_text('a',4)} {self.get_text('b',4)} {self.get_text('c',4)} {self.get_text('d',4)} {self.get_text('e',4)} {self.get_text('f',4)} {self.get_text('g',4)} {self.get_text('h',4)}|4  {d_b[8]} {d_b[9]}\n{d_w[8]} {d_w[9]}    3|{self.get_text('a',3)} {self.get_text('b',3)} {self.get_text('c',3)} {self.get_text('d',3)} {self.get_text('e',3)} {self.get_text('f',3)} {self.get_text('g',3)} {self.get_text('h',3)}|3  {d_b[6]} {d_b[7]}\n{d_w[10]} {d_w[11]}    2|{self.get_text('a',2)} {self.get_text('b',2)} {self.get_text('c',2)} {self.get_text('d',2)} {self.get_text('e',2)} {self.get_text('f',2)} {self.get_text('g',2)} {self.get_text('h',2)}|2  {d_b[4]} {d_b[5]}\n{d_w[12]} {d_w[13]}    1|{self.get_text('a',1)} {self.get_text('b',1)} {self.get_text('c',1)} {self.get_text('d',1)} {self.get_text('e',1)} {self.get_text('f',1)} {self.get_text('g',1)} {self.get_text('h',1)}|1  {d_b[2]} {d_b[3]}\n{d_w[14]} {d_w[15]}    0|{self.get_text('a',0)} {self.get_text('b',0)} {self.get_text('c',0)} {self.get_text('d',0)} {self.get_text('e',0)} {self.get_text('f',0)} {self.get_text('g',0)} {self.get_text('h',0)}|0  {d_b[0]} {d_b[1]}\n         a b c d e f g h"


        return text

    def __str__(self):
        return self._print_text()

    def _make_move(self, t):
        return Move(self.grid[t[0]][int(t[1])], self.grid[t[2]][int(t[3])])




# b = Board()
# b.move(Move(b.grid['a'][1], b.grid['a'][3]))
# b.white.capture(b.grid['a'][0].piece)
# b.black.capture(b.grid['h'][6].piece)
# print(b)

        
