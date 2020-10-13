class Square():
    def __init__(self, col, row):
        self.piece = None
        self.r = None
        self.l = None
        self.u = None
        self.d = None
        self.col = col
        self.row = row

    def add_piece(self, piece):
        self.piece = piece
        piece.place = self
    
    @property
    def ur(self):
        if self.u is None:
            if self.r is None:
                return None
            return self.r.u
        return self.u.r

    @property
    def ul(self):
        if self.u is None:
            if self.l is None:
                return None
            return self.l.u
        return self.u.l

    @property
    def dl(self):        
        if self.d is None:
            if self.l is None:
                return None
            return self.l.d
        return self.d.l

    @property
    def dr(self):
        if self.d is None:
            if self.r is None:
                return None
            return self.r.d
        return self.d.r
        
    @property
    def ru(self):
        return self.ur()

    @property
    def lu(self):
        return self.ul()

    @property
    def rd(self):
        return self.dr()

    @property
    def ld(self):
        return self.dl()

    def __str__(self):
        return f'Sq at {self.col}{self.row} with  {self.piece.name if self.piece else self.piece}'

    def __repr__(self):
        return f'<Square {self.col}{self.row}>'