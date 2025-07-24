import java.awt.Dimension;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Graphics {
    private final List<Img> frames = new ArrayList<>();
    private final boolean loop;
    private final double fps;
    private final double frameDurationMs;
    private long startMs;
    private int curFrame;

    public Graphics(Path spritesFolder, Dimension cellSize, boolean loop, double fps) {
        this.loop = loop;
        this.fps = fps;
        this.frameDurationMs = 1000.0 / fps;
        // load sprites PNGs in alphabetical order
        try (java.util.stream.Stream<java.nio.file.Path> paths = java.nio.file.Files.list(spritesFolder)) {
            paths.filter(p -> p.toString().endsWith(".png"))
                 .sorted()
                 .forEach(p -> frames.add(new Img().read(p.toString(), cellSize, true, null)));
        } catch (java.io.IOException ignored) {}
        if (frames.isEmpty()) {
            // create single blank frame placeholder
            java.awt.image.BufferedImage blank = new java.awt.image.BufferedImage(cellSize.width, cellSize.height, java.awt.image.BufferedImage.TYPE_INT_ARGB);
            Img img = new Img();
            try {
                java.lang.reflect.Field f = Img.class.getDeclaredField("img");
                f.setAccessible(true);
                f.set(img, blank);
            } catch (Exception e) { throw new RuntimeException(e); }
            frames.add(img);
        }
    }

    public void reset(Command cmd) {
        this.startMs = cmd.timestamp;
        this.curFrame = 0;
    }

    public void update(long nowMs) {
        long elapsed = nowMs - startMs;
        int framesPassed = (int) (elapsed / frameDurationMs);
        if (loop) {
            curFrame = framesPassed % frames.size();
        } else {
            curFrame = Math.min(framesPassed, frames.size() - 1);
        }
    }

    public Img getImg() {
        if (frames.isEmpty()) throw new IllegalStateException("No frames loaded for animation.");
        return frames.get(curFrame);
    }

    // For tests – allow direct access to frames
    public List<Img> getFrames() { return frames; }
    public int getCurFrame() { return curFrame; }
} 