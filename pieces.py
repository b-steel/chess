from chars import chars
class Pawn():
    def __init__(self, square, direction, team):
        self.team = team
        self.sq = square
        self.name = 'Pawn'
        self.moved = False
        self.char = chars[self.name]
        self.dir = direction

    def moves(self):
        if self.dir > 0:
            #regular orientation
            m = [sq for sq in [self.sq.u, self.sq.ur, self.sq.ul] if (sq.piece and sq.piece.team == self.team)]
            #move two on first move
            if ((self.sq.d.d is None) and (self.sq.u is None) and (self.sq.u.u.team != self.team)):
                m.append(self.sq.u.u)

        else:
            #reverse orientation 
            m = [sq for sq in [self.sq.d, self.sq.dr, self.sq.dl] if (sq.piece and sq.piece.team == self.team)]
            #move two on first move
            if ((self.sq.u.u is None) and (self.sq.d is None) and (self.sq.d.d.team != self.team)):
                m.append(self.sq.d.d)

        return m

class Rook():
    def __init__(self, square, direction, team):
        self.team = team
        self.sq = square
        self.name = 'rook'
        self.moved = False
        self.char = chars[self.name]
        self.dir = direction

    def moves(self): 
        m = []
        for d in ['r', 'l', 'u', 'd']:
            sq = getattr(self.sq, d)
            while (sq is not None) and (not sq.piece):
                m.append(sq)
                sq = getattr(sq, d) #next sq (square)
        return m
            


class Knight():
    def __init__(self, square, direction, team):
        self.team = team
        self.sq = square
        self.name = 'knight'
        self.moved = False
        self.char = chars[self.name]
        self.dir = direction

    def moves(self): 
        m = []
        for d1, d2 in zip(['u', 'u', 'd', 'd', 'l', 'l', 'r', 'r'], ['l', 'r', 'l', 'r', 'u', 'd', 'u', 'd']):
            s1 = getattr(self.sq, d1)
            if s1:
                s2 = getattr(s1, d1)
                if s2:
                    s3 = getattr(s2, d2)
                    if s3 and s3.piece.team != self.team:
                        m.append(s3)
        return m

class Bishop():
    def __init__(self, square, direction, team):
        self.team = team
        self.sq = square
        self.name = 'bishop'
        self.moved = False
        self.char = chars[self.name]
        self.dir = direction

    def moves(self): 
        m = []
        for d in ['ur', 'ul', 'dr', 'dl']:
            sq = getattr(self.sq, d)
            while (sq is not None) and (not sq.piece):
                m.append(sq)
                sq = getattr(sq, d) #next sq (square)
        return m

class Queen():
    def __init__(self, square, direction, team):
        self.team = team
        self.sq = square
        self.name = 'queen'
        self.moved = False
        self.char = chars[self.name]
        self.dir = direction

    def moves(self):
        m = []
        for d in ['r', 'l', 'u', 'd', 'ur', 'ul', 'dr', 'dl']:
            sq = getattr(self.sq, d)
            while (sq is not None) and (not sq.piece):
                m.append(sq)
                sq = getattr(sq, d) #next sq (square)
        return m 
        

class King():
    def __init__(self, square, direction, team):
        self.team = team
        self.sq = square
        self.name = 'king'
        self.moved = False
        self.char = chars[self.name]
        self.dir = direction
    
    def check(self, sqare = self.sq):
        pass


    def checkmate(self):
        return self.moves() is []

    def moves(self): 
        m = []
        for d in ['r', 'l', 'u', 'd', 'ur', 'ul', 'dr', 'dl']:
            sq = getattr(self.sq, d)
            if (sq is not None) and (not sq.piece) and (not self.check(sq)):
                m.append(sq)
        return m 

    def castle(self):
        '''returns if you can castle'''
        pass
