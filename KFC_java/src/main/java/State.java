import java.util.HashMap;
import java.util.Map;

public class State {
    public Moves moves;            // optional may be null
    public Graphics graphics;
    public Physics physics;
    private final Map<String, State> transitions = new HashMap<>();
    public String name;

    public State(Moves moves, Graphics graphics, Physics physics) {
        this.moves = moves;
        this.graphics = graphics;
        this.physics = physics;
    }

    @Override public String toString() { return "State(" + name + ")"; }

    public void setTransition(String event, State target) { transitions.put(event.toLowerCase(), target); }

    public Map<String, State> getTransitions() { return transitions; }

    public void reset(Command cmd) {
        graphics.reset(cmd);
        physics.reset(cmd);
    }

    public State onCommand(Command cmd, java.util.Map<Moves.Pair, java.util.List<Piece>> cell2piece) {
        String key = cmd.type.toLowerCase();
        if (transitions.containsKey(key) && (key.equals("done") || (cmd.params != null && !cmd.params.isEmpty()))) {
            State next = transitions.get(key);
            next.reset(cmd);
            return next;
        }
        return this;
    }

    public State update(long nowMs) {
        Command internal = physics.update(nowMs);
        if (internal != null) {
            return onCommand(internal, null);
        }
        return this;
    }

    public boolean canBeCaptured() { return physics.canBeCaptured(); }
    public boolean canCapture() { return physics.canCapture(); }
} 