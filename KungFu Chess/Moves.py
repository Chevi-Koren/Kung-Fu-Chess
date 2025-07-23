# Moves.py
from __future__ import annotations
import pathlib
from typing import List, Tuple

_CAPTURE     = 1   # tag flag
_NON_CAPTURE = 0


class Moves:
    """
    Parse moves.txt lines (whitespace & comments allowed):
        dr,dc               # can both capture and not capture
        dr,dc:non_capture   # non-capture move only
        dr,dc:capture       # capture move only (e.g. pawn diagonal)
    """
    def __init__(self, txt_path: pathlib.Path, dims: Tuple[int, int]):
        self.rel_moves: List[Tuple[int,int,int]] = self._load_moves(txt_path)
        self.W, self.H = dims

    def _load_moves(self, fp: pathlib.Path) -> List[Tuple[int,int,int]]:
        moves: List[Tuple[int,int,int]] = []
        with open(fp, encoding="utf-8") as f:
            for line in f:
                if line.strip() and not line.lstrip().startswith("#"):
                    moves.append(self._parse(line))
        return moves

    @staticmethod
    def _parse(s: str) -> Tuple[int,int,int]:
        if ":" not in s:
            raise ValueError(f"Unsupported move syntax: '{s.strip()}' – ':' required")

        coords, tag_str = s.split(":", 1)
        dr, dc = [int(x) for x in coords.split(",")]

        if tag_str.strip() == "capture":    # capture move only
            tag = _CAPTURE
        elif tag_str.strip() == "non_capture":  # non-capture move only 
            tag = _NON_CAPTURE
        else:   # can both capture and not capture
            tag = -1 # Default to -1 for "can both"

        return dr, dc, tag

    def is_dst_cell_valid(self, dr, dc, dst_has_piece):
        for move in self.rel_moves:
            if move[0] == dr and move[1] == dc:
                tag = move[2]
                if tag == -1: # "can both"
                    return True
                elif tag == _NON_CAPTURE:
                    return not dst_has_piece
                elif tag == _CAPTURE:
                    return dst_has_piece
                else:
                    raise ValueError(f"Invalid move tag: {tag}")
        return False
    
    def _path_is_clear(self, src, dst, cell2piece):
        import numpy as np

        # Get cell size in meters (assuming square cells)
        cell_H = self.board.cell_H_m
        cell_W = self.board.cell_W_m
        step_size = min(cell_H, cell_W) / 2

        src = np.array(src, dtype=float)
        dst = np.array(dst, dtype=float)
        direction = dst - src
        distance = np.linalg.norm(direction)
        if distance == 0:
            return True
        direction_unit = direction / distance

        num_steps = int(distance / step_size)
        for i in range(1, num_steps + 1):
            pos = src + direction_unit * step_size * i
            cell = self.board.m_to_cell(tuple(pos))
            if cell in cell2piece and cell2piece[cell].is_movement_blocker():
                return False
        return True

    def is_valid(self, src_cell, dst_cell, cell2piece):
        dr, dc = dst_cell[0] - src_cell[0], dst_cell[1] - src_cell[1]
        dst_has_piece = cell2piece.get(dst_cell) is not None
        if not self.is_dst_cell_valid(dr, dc, dst_has_piece):
            return False
        
        if not self._path_is_clear(src_cell, dst_cell):
            return False
        
        return True

        
