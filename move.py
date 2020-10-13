class Move():
    def __init__(self, piece, start, end):
        self.piece = piece
        self.start = start
        self.end = end
        self.capture = end.piece if end.piece else None