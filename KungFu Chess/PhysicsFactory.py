from Board import Board
from Physics import IdlePhysics, MovePhysics, JumpPhysics, RestPhysics, Physics


class PhysicsFactory:
    """Instantiate the correct *Physics* subclass for a given state."""

    def __init__(self, board: Board):
        self.board = board

    def create(self, start_cell, state_name: str, cfg) -> Physics:
        speed = cfg.get("speed_m_per_sec", 0.0)

        name_l = state_name.lower()
        if name_l == "move" or name_l.endswith("_move"):
            cls = MovePhysics
        elif name_l == "jump":
            cls = JumpPhysics
        elif name_l.endswith("rest") or name_l == "rest":
            cls = RestPhysics
        else:
            cls = IdlePhysics

        if cls is RestPhysics:
            duration_ms = cfg.get("duration_ms", 3000)
            return cls(start_cell, self.board, duration_ms)  # type: ignore[arg-type]

        return cls(start_cell, self.board, speed)
