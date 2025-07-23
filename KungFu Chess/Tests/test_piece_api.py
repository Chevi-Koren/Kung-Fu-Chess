import pytest
from Piece import Piece
from State import State
from Physics import Physics
from Command import Command

class DummyMoves:
    def get_moves(self,*_):
        return {(0,0)}

class DummyGraphics:
    def reset(self,*_):...
    def update(self,*_):...
    def get_img(self): return None

class DummyBoard:
    def __init__(self):
        self.cell_W_pix=self.cell_H_pix=70
        self.W_cells=self.H_cells=8
        self.img=None

def test_current_cell_accessor():
    board=DummyBoard()
    phys=Physics((2,3),board)
    st=State(DummyMoves(),DummyGraphics(),phys)
    p=Piece("PX",st)
    assert p.current_cell()==(2,3)
    # after issuing a Move, current_cell is still original until arrival
    cmd=Command(0,"PX","move",[(4,5)])
    st.reset(cmd)
    assert p.current_cell()==(2,3)

    # simulate time passing so Physics arrives
    phys_end = phys.start_ms + phys.duration_ms + 1
    phys.update(phys_end)
    assert p.current_cell()==(4,5) 