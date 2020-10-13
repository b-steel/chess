from chars import chars
from player import Player
from move import Move
class Piece():
    
    def __str__(self):
        return f'{self.player.color.capitalize()} {self.name.capitalize()} at {self.place.col}{self.place.row}'

class Pawn(Piece):
    def __init__(self, player):
        self.player = player
        self.place = None
        self.moved = False
        self.name = 'pawn'
        self.char = chars[self.player.color][self.name]
        self.direction = 1


    def available_moves(self, board):
        if self.direction == 1:
            place = self.place
            m = [sq for sq in [place.u] if sq and not sq.piece]
            m.append([sq for sq in [place.ur, place.ul] if sq and sq.piece and sq.piece.player != self.player])
        
            #move two on first move
            if (not self.moved and not place.u.piece and not place.u.u.piece):
                m.append(place.u.u)

            #En Passant Left
            if place.l and place.l.piece and isinstance(place.l.piece, Pawn) and place.l.piece.player != self.player: #enemy pawn to the left
                if board.last_turn.piece is place.l.piece: #that pawn was moved last turn
                    if board.last_turn.start is place.l.u.u: #the pawn moved two spaces
                        m.append(place.ul)

            #En Passant Right
            if place.r and place.r.piece and isinstance(place.r.piece, Pawn) and place.r.piece.player != self.player: #enemy pawn to the right
                if board.last_turn.piece is place.r.piece: #that pawn was moved last turn
                    if board.last_turn.start is place.r.u.u: #the pawn moved two spaces
                        m.append(place.ur)
        else:
            #OTHER DIRECTION
            place = self.place
            m = [sq for sq in [place.d] if sq and not sq.piece]
            m.append([sq for sq in [place.dr, place.dl] if sq and sq.piece and sq.piece.player != self.player])
        
            #move two on first move
            if (not self.moved and not place.d.piece and not place.d.d.piece):
                m.append(place.d.d)

            #En Passant Left
            if place.l and place.l.piece and isinstance(place.l.piece, Pawn) and place.l.piece.player != self.player: #enemy pawn to the left
                if board.last_turn.piece is place.l.piece: #that pawn was moved last turn
                    if board.last_turn.start is place.l.d.d: #the pawn moved two spaces
                        m.append(place.dl)

            #En Passant Right
            if place.r and place.r.piece and isinstance(place.r.piece, Pawn) and place.r.piece.player != self.player: #enemy pawn to the right
                if board.last_turn.piece is place.r.piece: #that pawn was moved last turn
                    if board.last_turn.start is place.r.d.d: #the pawn moved two spaces
                        m.append(place.dr)
        return m

class Rook(Piece):
    def __init__(self, player):
        self.player = player
        self.place = None
        self.moved = False
        self.name = 'rook'
        self.char = chars[self.player.color][self.name]


    def available_moves(self, board):
        place = self.place
        m = []
        for d in ['r', 'l', 'u', 'd']:
            sq = getattr(place, d)
            while (sq is not None) and (not sq.piece):
                m.append(sq)
                sq = getattr(sq, d) #next sq (square)
            if sq and sq.piece and sq.piece.player != self.player:
                m.append(sq)
        return m
            


class Knight(Piece):
    def __init__(self, player):
        self.player = player
        self.place = None
        self.moved = False
        self.name = 'knight'
        self.char = chars[self.player.color][self.name]


    def available_moves(self, board):
        place = self.place
        m = []
        for d1, d2 in zip(['u', 'u', 'd', 'd', 'l', 'l', 'r', 'r'], ['l', 'r', 'l', 'r', 'u', 'd', 'u', 'd']):
            s1 = getattr(place, d1)
            if s1: 
                s2 = getattr(s1, d1)
                if s2: 
                    s3 = getattr(s2, d2)
                    if s3 and (not s3.piece or s3.piece and s3.piece.player != self.player):
                        m.append(s3)
        return m

class Bishop(Piece):
    def __init__(self, player):
        self.player = player
        self.place = None
        self.moved = False
        self.name = 'bishop'
        self.char = chars[self.player.color][self.name]


    def available_moves(self, board):
        place = self.place
        m = []
        for d in ['ur', 'ul', 'dr', 'dl']:
            sq = getattr(place, d)
            while (sq is not None) and (not sq.piece):
                m.append(sq)
                sq = getattr(sq, d) #next sq (square)
            if sq and sq.piece and sq.piece.player != self.player:
                m.append(sq)
        return m

class Queen(Piece):
    def __init__(self, player):
        self.player = player
        self.place = None
        self.moved = False
        self.name = 'queen'
        self.char = chars[self.player.color][self.name]


    def available_moves(self, board):
        place = self.place
        m = []
        for d in ['r', 'l', 'u', 'd', 'ur', 'ul', 'dr', 'dl']:
            sq = getattr(place, d)
            while (sq is not None) and (not sq.piece):
                m.append(sq)
                sq = getattr(sq, d) #next sq (square)
            if sq and sq.piece and sq.piece.player != self.player:
                m.append(sq)    
        return m 
        

class King(Piece):
    def __init__(self, player):
        self.player = player
        self.place = None
        self.moved = False
        self.name = 'king'
        self.char = chars[self.player.color][self.name]
    
    def check(self, square, board):
        for piece in self.player.opponent.pieces:
            if isinstance(piece, King):
                for d in ['u', 'd', 'l', 'r', 'ur', 'ul', 'dr', 'dl']:
                    if getattr(piece.place, d) is self.place:
                        return True
            else:
                if square in piece.available_moves(board):
                    return True
        return False
            
    def available_moves(self, board):
        place = self.place
        m = []
        for d in ['r', 'l', 'u', 'd', 'ur', 'ul', 'dr', 'dl']:
            sq = getattr(place, d)
            if sq and (not sq.piece or sq.piece.player != self.player):
                m.append(sq)
        m.extend(self.castle(board))
        for sq in m:
            if self.check(sq, board):
                m.remove(sq)
        return m 

    def castle(self, board):
        '''returns the rooks you can castle with '''
        if self.moved: return []
        return [p for p in self.player.pieces if isinstance(p, Rook) and not p.moved]
        
