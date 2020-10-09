from chars import chars
from team import Team
class Piece():
    def __init__(self):
        self.team = None
        self.place = None
        self.name = ''
        self.moved = False
        self.char = None
    
    def __str__(self):
        return f'{self.name.capitalize()} Piece at {self.place.col}{self.place.row} on team {self.team.color}'

class Pawn(Piece):
    def __init__(self, direction):
        self.team = None
        self.place = None
        self.name = 'pawn'
        self.moved = False
        self.char = None
        self.dir = direction

    def moves(self):
        if self.dir > 0:
            #regular orientation
            m = [sq for sq in [self.place.u] if sq and not sq.piece]
            m.append([sq for sq in [self.place.ur, self.place.ul] if sq and sq.piece and sq.piece.team !=self.team])
        
            #move two on first move
            if (self.place.d.d is None and not self.place.u.piece and not self.place.u.u.piece):
                m.append(self.place.u.u)

        else:
            #reverse orientation 
            m = [sq for sq in [self.place.d] if sq and not sq.piece]
            m.append([sq for sq in [self.place.dr, self.place.dl] if sq and sq.piece and sq.piece.team !=self.team])
        
            #move two on first move
            if (self.place.u.u is None and not self.place.d.piece and not self.place.d.d.piece):
                m.append(self.place.d.d)

        return m

class Rook(Piece):
    def __init__(self, direction):
        self.team = None
        self.place = None
        self.name = 'rook'
        self.moved = False
        self.char = None
        self.dir = direction

    def moves(self): 
        m = []
        for d in ['r', 'l', 'u', 'd']:
            sq = getattr(self.place, d)
            while (sq is not None) and (not sq.piece):
                m.append(sq)
                sq = getattr(sq, d) #next sq (square)
            if sq and sq.piece and sq.piece.team != self.team:
                m.append(sq)
        return m
            


class Knight(Piece):
    def __init__(self, direction):
        self.team = None
        self.place = None
        self.name = 'knight'
        self.moved = False
        self.char = None
        self.dir = direction

    def moves(self): 
        m = []
        for d1, d2 in zip(['u', 'u', 'd', 'd', 'l', 'l', 'r', 'r'], ['l', 'r', 'l', 'r', 'u', 'd', 'u', 'd']):
            s1 = getattr(self.place, d1)
            if s1:
                s2 = getattr(s1, d1)
                if s2:
                    s3 = getattr(s2, d2)
                    if s3 and (not s3.piece or s3.piece and s3.piece.team != self.team):
                        m.append(s3)
        return m

class Bishop(Piece):
    def __init__(self, direction):
        self.team = None
        self.place = None
        self.name = 'bishop'
        self.moved = False
        self.char = None
        self.dir = direction

    def moves(self): 
        m = []
        for d in ['ur', 'ul', 'dr', 'dl']:
            sq = getattr(self.place, d)
            while (sq is not None) and (not sq.piece):
                m.append(sq)
                sq = getattr(sq, d) #next sq (square)
            if sq and sq.piece and sq.piece.team != self.team:
                m.append(sq)
        return m

class Queen(Piece):
    def __init__(self, direction):
        self.team = None
        self.place = None
        self.name = 'queen'
        self.moved = False
        self.char = None
        self.dir = direction

    def moves(self):
        m = []
        for d in ['r', 'l', 'u', 'd', 'ur', 'ul', 'dr', 'dl']:
            sq = getattr(self.place, d)
            while (sq is not None) and (not sq.piece):
                m.append(sq)
                sq = getattr(sq, d) #next sq (square)
            if sq and sq.piece and sq.piece.team != self.team:
                m.append(sq)    
        return m 
        

class King(Piece):
    def __init__(self, direction):
        self.team = None
        self.place = None
        self.name = 'king'
        self.moved = False
        self.char = None
        self.dir = direction
    
    def check(self, square):
        for piece in self.team.opponent.pieces:
            if square in piece.moves():
                return True
        return False


    def checkmate(self):
        return self.moves() is []

    def moves(self): 
        m = []
        for d in ['r', 'l', 'u', 'd', 'ur', 'ul', 'dr', 'dl']:
            sq = getattr(self.place, d)
            if sq and (not sq.piece or sq.piece.team != self.team) and (not self.check(sq)):
                m.append(sq)
        return m 

    def castle(self):
        '''returns if you can castle'''
        pass
