class Move():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.piece = start.piece
        self.capture = end.piece if end.piece else None
