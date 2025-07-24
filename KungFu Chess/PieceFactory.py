# PieceFactory.py
from __future__ import annotations
import csv, json, pathlib
from plistlib import InvalidFileException
from typing import Dict, Tuple

from Board           import Board
from Command         import Command
from GraphicsFactory import GraphicsFactory
from Moves           import Moves
from PhysicsFactory  import PhysicsFactory
from Piece           import Piece
from State           import State


class PieceFactory:
    def __init__(self,
                 board: Board,
                 graphics_factory=None,
                 physics_factory=None):
                 
        self.board            = board
        self.graphics_factory = graphics_factory or GraphicsFactory()
        self.physics_factory  = physics_factory or PhysicsFactory(board)
        self.templates: Dict[str, State] = {}
        self._global_trans: dict[str, dict[str, str]] = {}

    # ──────────────────────────────────────────────────────────────
    def _load_master_csv(self, pieces_root: pathlib.Path) -> None:
        if self._global_trans:                     # already read
            return
        csv_path = pieces_root / "transitions.csv"
        if not csv_path.exists():
            return

        with csv_path.open(newline="", encoding="utf-8") as f:
            rdr = csv.DictReader(f)
            for row in rdr:
                frm, ev, nxt = row["from_state"], row["event"], row["to_state"]
                self._global_trans.setdefault(frm, {})[ev] = nxt

    # ──────────────────────────────────────────────────────────────
    def generate_library(self, pieces_root: pathlib.Path) -> None:
        self._load_master_csv(pieces_root)
        for sub in pieces_root.iterdir():          # “PW”, “KN”, …
            if sub.is_dir():
                self.templates[sub.name] = self._build_state_machine(sub)

    # ──────────────────────────────────────────────────────────────
    def _build_state_machine(self, piece_dir: pathlib.Path) -> State:
        board_size = (self.board.W_cells, self.board.H_cells)
        cell_px    = (self.board.cell_W_pix, self.board.cell_H_pix)

        states: Dict[str, State] = {}

        # There is no longer a piece-wide fall-back. Each state must provide its own
        # `moves.txt`; if it does not, the state will have *no* legal moves.
        # ── load every <piece>/states/<state>/ ───────────────────
        for state_dir in (piece_dir / "states").iterdir():
            if not state_dir.is_dir():
                continue
            name = state_dir.name

            cfg_path = state_dir / "config.json"
            cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}

            moves_path = state_dir / "moves.txt"
            moves = Moves(moves_path, board_size) if moves_path.exists() else None
            graphics = self.graphics_factory.load(state_dir / "sprites",
                                                  cfg.get("graphics", {}), cell_px)
            physics  = self.physics_factory.create((0, 0), name, cfg.get("physics", {}))

            st = State(moves, graphics, physics)
            st.name = name
            states[name] = st

        # apply master CSV overrides
        for frm, ev_map in self._global_trans.items():
            src = states.get(frm)
            if not src:
                continue
            for ev, nxt in ev_map.items():
                dst = states.get(nxt)
                if not dst:
                    continue

                src.set_transition(ev, dst)

        # always start at idle
        return states.get("idle")

    # ──────────────────────────────────────────────────────────────
    def create_piece(self, p_type: str, cell: Tuple[int, int]) -> Piece:
        template_idle = self.templates[p_type]

        # Each state will have its own physics object; no shared instance.
        clone_map: Dict[State, State] = {}
        stack = [template_idle]
        while stack:
            orig = stack.pop()
            if orig in clone_map:
                continue
            new_phys = self.physics_factory.create(cell, orig.name, {})
            clone = State(orig.moves,
                          orig.graphics.copy(),
                          new_phys)
            clone.name = orig.name
            clone_map[orig] = clone
            stack.extend(orig.transitions.values())

        # re‑wire transitions
        for orig, clone in clone_map.items():
            for ev, target in orig.transitions.items():
                clone.set_transition(ev, clone_map[target])

        piece = Piece(f"{p_type}_{cell}", clone_map[template_idle])
        # initialise physics position
        piece.state.reset(Command(0, piece.id, "idle", [cell]))
        return piece
