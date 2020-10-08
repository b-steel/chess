class Captured():
    def __init__(self):
        self.pieces = []
    
    def add_piece(self, piece):
        self.pieces.append(piece)
        piece.place = self

class Square():
    def __init__(self):
        self.piece = None
        self.r = None
        self.l = None
        self.u = None
        self.d = None

    def add_piece(self, piece):
        assert self.pieces is None
        self.pieces = piece
        piece.place = self
    
    @property
    def ur(self):
        try:
            return self.u.r
        except Exception:
            pass
        try:
            return self.r.u
        except Exception:
            pass
        finally:
            return None

    @property
    def ul(self):
        try:
            return self.u.l
        except Exception:
            pass
        try:
            return self.l.u
        except Exception:
            pass
        finally:
            return None

    @property
    def dl(self):
        try:
            return self.d.l
        except Exception:
            pass
        try:
            return self.l.d
        except Exception:
            pass
        finally:
            return None

    @property
    def dr(self):
        try:
            return self.d.r
        except Exception:
            pass
        try:
            return self.r.d
        except Exception:
            pass
        finally:
            return None
