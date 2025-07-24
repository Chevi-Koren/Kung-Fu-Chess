import java.util.List;

public class Command {
    public final long timestamp;   // milliseconds since game start
    public final String pieceId;
    public final String type;      // e.g. "move", "jump", "idle", "done"
    public final List<Object> params;

    public Command(long timestamp, String pieceId, String type, List<Object> params) {
        this.timestamp = timestamp;
        this.pieceId = pieceId;
        this.type = type;
        this.params = params;
    }
} 