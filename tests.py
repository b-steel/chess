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