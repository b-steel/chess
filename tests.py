from mamba import description, context, it, before, after
from expects import equal, expect, be_a, be, have_len, be_true
from places import Square
from board import Board
from pieces import *
from game import Game

with description('game') as self:
    with before.all:
        self.g = Game()
        self.pawn1 = self.g.board.grid['f'][1].piece
        self.pawn2 = self.g.board.grid['e'][6].piece

        for mv in ['f1 f3', 'e6 e4', 'f3 e4']:
            self.g.board.move(self.g.parse_input(mv))
            self.g.show()

    with it('captures pawns'):
        captured = self.g.board.dead_white
        expect(self.pawn2.place).to(be(captured))

    







