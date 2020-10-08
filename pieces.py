from chars import chars

class Piece():
    def __init__(self):
        self.place = None
        self.team = None

class Pawn(Piece):
    def __init__(self):
        super.__init__()
        self.name = 'Pawn'
        self.moved = False
        self.char = chars[self.name]


