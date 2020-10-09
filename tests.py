from mamba import description, context, it, before, after
from expects import equal, expect, be_a, be, have_len
from places import Square
from board import Board
from pieces import *

with description('Square') as self:
    with before.each:
            
        self.sq = Square()
        self.sl = Square()
        self.sr = Square()
        self.su = Square()
        self.sd = Square()
        self.sur = Square()
        self.sul = Square()
        self.sq.u = self.su
        self.sq.d = self.sd
        self.sq.l = self.sl
        self.sq.r = self.sr
        self.su.r = self.sur
        self.sr.u = self.sur
        self.su.l = self.sul
        self.sl.u = self.sul
    with it('@property methods work'):
        expect(self.sq.ur).to(be(self.sur))
        expect(self.sq.ul).to(be(self.sul))
        expect(self.sq.dr).to(be(None))
        expect(self.sq.dl).to(be(None))

    with it('@property methods are calculated each time'):
        expect(self.sq.ur).to(be(self.sur))
        self.sq.u.r = None
        self.sq.r.u = None
        expect(self.sq.ur).to(be(None))

    with it('properties are calculated both ways'):
        self.sq.u = None
        expect(self.sq.ur).to(be(self.sur))


with description('Board') as self:
    with context('create squares'):
        with before.each:
            self.b = Board()

        with it('has right size'):
            expect(self.b.grid).to(have_len(8))
            expect(self.b.grid[2]).to(have_len(8))

        with it('has a square in each'):
            for row in range(8):
                for col in range(8):
                    expect(self.b.grid[row][col]).to(be_a(Square))

        with it('has squares that know their place correctly'):
            for row in range(6):
                for col in range(7):
                    expect(self.b.grid[row][col].ur).to(be(self.b.grid[row+1][col+1]))

    with context('create pieces'):
        with before.each:
            self.b = Board()

            with it('has pawns'):
                for col in range(8):
                    expect(self.b.grid[1][col].piece).to(be_a(Pawn))
                    expect(self.b.grid[6][col].piece).to(be_a(Pawn))
            with it('has other pieces'):
                for row in [0,7]:
                    expect(self.b.grid[row][0].piece).to(be_a(Rook))
                    expect(self.b.grid[row][7].piece).to(be_a(Rook))
                    expect(self.b.grid[row][1].piece).to(be_a(Knight))
                    expect(self.b.grid[row][6].piece).to(be_a(Knight))
                    expect(self.b.grid[row][2].piece).to(be_a(Bishop))
                    expect(self.b.grid[row][5].piece).to(be_a(Bishop))
                    expect(self.b.grid[row][3].piece).to(be_a(Queen))
                    expect(self.b.grid[row][4].piece).to(be_a(King))

            with it('has opposite teams'):
                expect(self.b.grid[0][3].piece.team.opponent).to(be(self.b.grid[6][0].piece.team))







