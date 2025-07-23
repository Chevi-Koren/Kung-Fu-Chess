import pathlib
from typing import List, Dict, Tuple, Optional

class Moves:
    def __init__(self, txt_path: pathlib.Path, dims: Tuple[int, int]):
        self.rel_moves = self._load_moves(txt_path)
        self.W, self.H = dims
        print(f"[LOAD] Moves from: {txt_path}")


    def _load_moves(self, fp) -> List[Tuple[int, int, int]]:
        with open(fp) as f:
            return [self._parse(l) for l in f if l.strip() and not l.lstrip().startswith("#")]

    def get_moves(self, r: int, c: int) -> List[Tuple[int, int]]:
        moves = []
        for mv in self.rel_moves:
            dr, dc = mv[0], mv[1]
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.H and 0 <= nc < self.W:
                moves.append((nr, nc))
        return moves

    @staticmethod
    def _parse(line: str) -> Tuple[int, int, int]:
        # 1️⃣ remove surrounding [ ] and any trailing comment
        clean = line.partition("#")[0].strip()  # drop inline comments
        clean = clean.strip("[] \n")  # remove brackets / NL

        # 2️⃣ turn commas into spaces and split
        parts = [int(x) for x in clean.replace(",", " ").split()]
        if len(parts) == 2:
            dr, dc = parts
            tag = -1  # -1 means “always allowed”
        elif len(parts) == 3:
            dr, dc, tag = parts
        else:
            raise ValueError(f"Bad moves.txt line: {line!r}")

        return dr, dc, tag



