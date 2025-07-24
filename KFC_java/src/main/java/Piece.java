import java.util.*;

public class Piece {
    public final String id;
    public State state;

    public Piece(String pieceId, State initState) {
        this.id = pieceId;
        this.state = initState;
    }

    public void onCommand(Command cmd, Map<Moves.Pair, List<Piece>> cell2piece) {
        state = state.onCommand(cmd, cell2piece);
    }

    public void reset(long startMs) {
        state.reset(new Command(startMs, id, "idle", List.of()));
    }

    public void update(long nowMs) {
        state = state.update(nowMs);
    }

    public boolean isMovementBlocker() {
        return state.physics.isMovementBlocker();
    }

    public void drawOnBoard(Board board, long nowMs) {
        int[] posPix = state.physics.getPosPix();
        Img sprite = state.graphics.getImg();
        sprite.drawOn(board.getImg(), posPix[0], posPix[1]);
    }

    public Moves.Pair currentCell() { return state.physics.getCurrCell(); }
} 