import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

public class Moves {

    private final int rows;
    private final int cols;
    private final Map<Pair, String> moves = new HashMap<>(); // (dr,dc) -> tag

    public Moves(Path movesFile, int rows, int cols) {
        this.rows = rows;
        this.cols = cols;
        if (Files.exists(movesFile)) {
            try (BufferedReader br = Files.newBufferedReader(movesFile)) {
                br.lines().forEach(line -> {
                    String l = line.strip();
                    if (l.isEmpty() || l.startsWith("#")) return;
                    String[] parts = l.split(":", 2);
                    String[] coords = parts[0].split(",");
                    int dr = Integer.parseInt(coords[0].trim());
                    int dc = Integer.parseInt(coords[1].trim());
                    String tag = parts.length > 1 ? parts[1].strip() : "";
                    moves.put(new Pair(dr, dc), tag);
                });
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public boolean isDstCellValid(int dr, int dc, boolean dstHasPiece) {
        String tag = moves.get(new Pair(dr, dc));
        if (tag == null) {
            // Unknown move – not allowed (Python version returns False)
            return false;
        }
        if (tag.isEmpty()) return true; // can both capture & non-capture
        switch (tag) {
            case "capture":
                return dstHasPiece;
            case "non_capture":
                return !dstHasPiece;
            default:
                return false;
        }
    }

    public boolean isValid(int[] srcCell, int[] dstCell, java.util.Set<Pair> occupiedCells) {
        int dstR = dstCell[0], dstC = dstCell[1];
        if (dstR < 0 || dstR >= rows || dstC < 0 || dstC >= cols) return false;
        int dr = dstR - srcCell[0];
        int dc = dstC - srcCell[1];
        boolean dstHasPiece = occupiedCells.contains(new Pair(dstR, dstC));
        if (!isDstCellValid(dr, dc, dstHasPiece)) return false;
        if (!pathIsClear(srcCell, dstCell, occupiedCells)) return false;
        return true;
    }

    private boolean pathIsClear(int[] srcCell, int[] dstCell, java.util.Set<Pair> occupiedCells) {
        int dr = dstCell[0] - srcCell[0];
        int dc = dstCell[1] - srcCell[1];
        if (Math.abs(dr) <= 1 && Math.abs(dc) <= 1) return true;
        int steps = Math.max(Math.abs(dr), Math.abs(dc));
        double stepR = dr / (double) steps;
        double stepC = dc / (double) steps;
        for (int i = 1; i < steps; i++) {
            int r = srcCell[0] + (int) Math.round(i * stepR);
            int c = srcCell[1] + (int) Math.round(i * stepC);
            if (occupiedCells.contains(new Pair(r, c))) return false;
        }
        return true;
    }

    /* simple record for coordinate pairs */
    public static class Pair {
        public final int r;
        public final int c;
        public Pair(int r, int c) { this.r = r; this.c = c; }
        @Override public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Pair)) return false;
            Pair other = (Pair) o;
            return r == other.r && c == other.c;
        }
        @Override public int hashCode() {
            return 31 * r + c;
        }
        @Override public String toString() { return "("+r+","+c+")"; }
    }
} 