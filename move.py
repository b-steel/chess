class Move():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.piece = start.piece
        self.capture = end.piece if end.piece else None
    
    def __str__(self):
        return f'<Move: {self.piece.player.color} {self.piece.name} {self.start.col}{self.start.row} -> {self.end.col}{self.end.row}>'