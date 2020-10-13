from mamba import description, context, it, before, after
from expects import equal, expect, be_a, be, have_len, be_true, contain
from places import Square
from board import Board
from pieces import *
from move import Move
from game import Game

with description('board') as self:

    with it('allows en passant as an option'):
        b = Board()

        m1 = b._make_move('a1a4')
        b.move(m1)

        m2 = b._make_move('b6b4')
        b.move(m2)

        expect(b.grid['a'][4].piece.available_moves(b)).to(
            contain(b.grid['b'][5]))

    with it('allows en passant only if the pawn move was last turn'):
        b = Board()

        m1 = b._make_move('a1a4')
        b.move(m1)

        m2 = b._make_move('b6b4')
        b.move(m2)

        m3 = b._make_move('g0h2')
        b.move(m3)

        expect(b.grid['a'][4].piece.available_moves(b)).to_not(contain(b.grid['b'][5]))

    with it('allows en passant only if the pawn moved two spaces'):
        b = Board()

        m1 = b._make_move('a1a4')
        b.move(m1)

        m2 = b._make_move('b6b5')
        b.move(m2)

        m3 = b._make_move('b5b6')
        b.move(m3)

        expect(b.grid['a'][4].piece.available_moves(b)).to_not(contain(b.grid['b'][5]))

    with it('allows pawns to en passant capture'):
        b = Board()

        m1 = b._make_move('a1a4')
        b.move(m1)

        m2 = b._make_move('b6b4')
        b.move(m2)

        captured_pawn = b.grid['b'][4].piece
        m3 = b._make_move('a4b5')
        

        expect(b.grid['b'][4].piece).to(be(None))
        expect(b.white.captured).to(contain(captured_pawn))
    







