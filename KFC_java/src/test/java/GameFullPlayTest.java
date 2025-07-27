import org.junit.jupiter.api.Test;
import java.nio.file.Path;
import static org.junit.jupiter.api.Assertions.*;

public class GameFullPlayTest {
    private static final Path PIECES_DIR = Path.of("..", "pieces");

    private void runLoops(Game game, int loops) {
        game._run_game_loop(loops, false);
    }

    @Test
    void testPawnMoveAndCapture() {
        Game game = GameFactory.createGame(PIECES_DIR);
        game.setTimeFactor(1_000_000_000L);
        game._update_cell2piece_map();

        Piece pw = game.pos.get(new Moves.Pair(6,0)).get(0);
        Piece pb = game.pos.get(new Moves.Pair(1,1)).get(0);

        game.userInputQueue.add(new Command(game.game_time_ms(), pw.id, "move", java.util.List.of(new Moves.Pair(6,0), new Moves.Pair(4,0))));
        game.userInputQueue.add(new Command(game.game_time_ms(), pb.id, "move", java.util.List.of(new Moves.Pair(1,1), new Moves.Pair(3,1))));

        runLoops(game, 200);

        assertEquals(new Moves.Pair(4,0), pw.currentCell());
        assertEquals(new Moves.Pair(3,1), pb.currentCell());

        game.userInputQueue.add(new Command(game.game_time_ms(), pw.id, "move", java.util.List.of(new Moves.Pair(4,0), new Moves.Pair(3,1))));
        runLoops(game, 200);

        assertEquals(new Moves.Pair(3,1), pw.currentCell());
        assertTrue(game.pieces.contains(pw));
        assertFalse(game.pieces.contains(pb));
    }
} 