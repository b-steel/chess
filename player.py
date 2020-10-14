from chars import chars
class Player():
    def __init__(self, color):
        self.pieces = []
        self.captured = []
        self.opponent = None
        self.color = color
        self.king = None
        self.direction = 1

    def add_piece(self, p):
        self.pieces.append(p)

    def capture(self, p):
        self.captured.append(p)
        p.place.piece = None
        p.place = f'Captured by {self.color}'
        p.player.pieces.remove(p)

    def __str__(self):
        return f'<Player: {self.color.capitalize()}>'