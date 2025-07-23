from __future__ import annotations
from ast import List, Tuple
from Command import Command
from Moves import Moves
from Graphics import Graphics
from Physics import Physics
from typing import Dict, Callable, Optional
import time, logging

from Piece import Piece

logger = logging.getLogger(__name__)


class State:
    def __init__(self, moves: Optional[Moves], graphics: Graphics, physics: Physics):
        self.moves: Optional[Moves] = moves
        self.graphics, self.physics = graphics, physics
        self.transitions: Dict[str, "State"] = {}
        self.name = None

    def __repr__(self):
        return f"State({self.name})"

    def set_transition(self, event: str, target: "State"):
        self.transitions[event] = target

    def reset(self, cmd: Command):
        self.graphics.reset(cmd)
        self.physics.reset(cmd)


    def get_state_after_command(self, cmd: Command, cell2piece: Dict[Tuple[int, int], List[Piece]]) -> State:
        
        nxt = self.transitions.get(cmd.type)

        if not nxt:
            return self
        
        if cmd.type == "move":
            if self.moves is None:
                return self
            
            src_cell = cmd.params[0]
            dst_cell = cmd.params[1]
            if src_cell != self.physics.get_curr_cell():
                logger.debug(f"Move rejected because source cell {src_cell} is not the current cell {self.physics.get_curr_cell()}")
                return self
            
            if not self.moves.is_valid(src_cell, dst_cell, cell2piece):
                return self
            
        logger.debug("[TRANSITION] %s: %s → %s", cmd.type, self, nxt)

        nxt.reset(cmd)
        return nxt


    def update(self, now_ms: int) -> State:
        internal = self.physics.update(now_ms)
        if internal:
            logger.debug("[DBG] internal:", internal.type)
            return self.get_state_after_command(internal, None)
        self.graphics.update(now_ms)
        return self


    def can_be_captured(self) -> bool:
        return self.physics.can_be_captured()

    def can_capture(self) -> bool:
        return self.physics.can_capture()
