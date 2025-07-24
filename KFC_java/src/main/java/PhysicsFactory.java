import org.json.JSONObject;

public class PhysicsFactory {
    private final Board board;
    public PhysicsFactory(Board board){ this.board=board; }

    public Physics create(Moves.Pair startCell, String stateName, JSONObject cfg){
        double speed = cfg.optDouble("speed_m_per_sec", 0.0);
        Physics phys;
        String name = stateName.toLowerCase();
        if(name.equals("move")||name.endsWith("_move")){
            phys = new Physics.MovePhysics(board, speed);
        } else if(name.equals("jump")){
            phys = new Physics.JumpPhysics(board, cfg.optDouble("duration_ms",100)/1000.0);
        } else if(name.endsWith("rest")||name.equals("rest")){
            phys = new Physics.RestPhysics(board, cfg.optDouble("duration_ms",3000)/1000.0);
        } else {
            phys = new Physics.IdlePhysics(board);
        }
        // initialise position
        phys.startCell = startCell;
        phys.currPosM = board.cellToM(startCell);
        return phys;
    }
} 