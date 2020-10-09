from chars import chars
class Team():
    def __init__(self, color):
        self.pieces = []
        self.opponent = None
        self.color = color
        self.king = None

    def add_piece(self, p):
        self.pieces.append(p)
        p.team = self
        p.char = chars[self.color][p.name]