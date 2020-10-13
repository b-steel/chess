from chars import chars
from team import Team
from move import Move
class Piece():
    
    def __str__(self):
        return f'{self.team.color} {self.name.capitalize()} at {self.place.col}{self.place.row}'

class Pawn(Piece):
    def __init__(self, player):
        self. = player
        self.place = None
        self.moved = False
        self.name = 'pawn'
        self.char = chars[self.player.color][self.name]


    def available_moves(self, board):
        place = self.place
        m = [sq for sq in [place.u] if sq and not sq.piece]
        m.append([sq for sq in [place.ur, place.ul] if sq and sq.piece and sq.piece.player != self.player])
    
        #move two on first move
        if (not self.moved and not place.u.piece and not place.u.u.piece):
            m.append(place.u.u)

        #En Passant Left
        if isinstance(place.l.piece, Pawn) and place.l.piece.player != self.player: #enemy pawn to the left
            if board.last_turn.move.piece is place.l.piece: #that pawn was moved last turn
                if board.last_turn.move.start is place.l.u.u: #the pawn moved two spaces
                    m.append(place.ul)

        #En Passant Righ
        if isinstance(place.r.piece, Pawn) and place.r.piece.player != self.player: #enemy pawn to the left
            if board.last_turn.move.piece is place.r.piece: #that pawn was moved last turn
                if board.last_turn.move.start is place.r.u.u: #the pawn moved two spaces
                    m.append(place.ur)

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
            if s1: s2 = getattr(s1, d1)
                if s2: s3 = getattr(s2, d2)
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
    
    def check(self, square):
        for piece in self.player.opponent.pieces:
            if square in piece.moves():
                return True
        return False
            
    def available_moves(self, board):
        place = self.place
        m = []
        for d in ['r', 'l', 'u', 'd', 'ur', 'ul', 'dr', 'dl']:
            sq = getattr(place, d)
            if sq and (not sq.piece or sq.piece.player != self.player):
                if not self.check(sq):
                    m.append(sq)
        m.extend(self.castle())
        return m 

    def castle(self):
        '''returns the rooks you can castle with '''
        if self.moved: return []
        return [p for p in self.player.pieces if isinstance(p, Rook) and not p.moved and not self.check(p.place)]
        
