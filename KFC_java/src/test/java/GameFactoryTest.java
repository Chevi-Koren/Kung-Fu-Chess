import org.junit.jupiter.api.Test;
import java.nio.file.Path;
import static org.junit.jupiter.api.Assertions.*;

public class GameFactoryTest {
    private static final Path PIECES_DIR = Path.of("..", "KungFu Chess", "pieces");

    @Test
    void testCreateGameBuildsFullBoard() {
        Game game = GameFactory.createGame(PIECES_DIR);
        assertNotNull(game);
        assertEquals(32, game.pieces.size());
    }

    @Test
    void testGraphicsFactoryLoadsSprites() {
        GraphicsFactory gf = new GraphicsFactory();
        Path spritesDir = PIECES_DIR.resolve(Path.of("PW", "states", "idle", "sprites"));
        Graphics gfx = gf.load(spritesDir, new org.json.JSONObject(), new java.awt.Dimension(32,32));
        assertFalse(gfx.getFrames().isEmpty());
        for (Img img : gfx.getFrames()) {
            assertTrue(img instanceof Img);
        }
    }
} 