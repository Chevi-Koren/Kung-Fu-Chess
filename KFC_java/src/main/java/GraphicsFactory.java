import java.awt.Dimension;
import java.nio.file.Path;
import org.json.JSONObject;

public class GraphicsFactory {
    public Graphics load(Path spritesDir, JSONObject cfg, Dimension cellSize) {
        boolean loop = cfg.optBoolean("is_loop", true);
        double fps = cfg.optDouble("frames_per_sec", 6.0);
        return new Graphics(spritesDir, cellSize, loop, fps);
    }
} 